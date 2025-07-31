# api/main.py

import os
import sys
import asyncio
import telegram
import decimal

# --- ADDED FOR DEBUGGING ---
print("--- STEP 1: Starting api/main.py ---")
sys.stdout.flush() # Forces the log to show immediately

from fastapi import FastAPI, Request, Response
from telegram.ext import Application
from dotenv import load_dotenv

# --- ADDED FOR DEBUGGING ---
print("--- STEP 2: Imports successful ---")
sys.stdout.flush()

from bot.handlers import start, deposit # Import your handlers
from bot.chapa_service import verify_payment
from database_models.models import User, Transaction, async_session

# --- ADDED FOR DEBUGGING ---
print("--- STEP 3: Local module imports successful ---")
sys.stdout.flush()

# Load environment variables
load_dotenv()

# --- ADDED FOR DEBUGGING ---
print("--- STEP 4: Loading environment variables from OS ---")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Check if the critical token is present
if not TELEGRAM_BOT_TOKEN:
    print("--- FATAL ERROR: TELEGRAM_BOT_TOKEN is not set! Exiting. ---")
    sys.stdout.flush()
    # In a real app, you'd exit more gracefully, but for debugging this is fine.
    exit(1)

print(f"--- STEP 5: TELEGRAM_BOT_TOKEN is present. ---")
sys.stdout.flush()

# --- FastAPI App Setup ---
print("--- STEP 6: Creating FastAPI app instance. ---")
sys.stdout.flush()
app = FastAPI()

print("--- STEP 7: Creating Telegram PTB Application instance. ---")
sys.stdout.flush()
ptb_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
print("--- STEP 8: PTB Application created successfully. ---")
sys.stdout.flush()


@app.on_event("startup")
async def startup_event():
    print("--- RUNNING STARTUP EVENT ---")
    # Register handlers
    ptb_app.add_handler(telegram.ext.CommandHandler("start", start))
    ptb_app.add_handler(telegram.ext.CommandHandler("deposit", deposit))

    # Set webhook
    if WEBHOOK_URL:
        print(f"--- Setting Telegram webhook to {WEBHOOK_URL}/api/telegram ---")
        await ptb_app.bot.set_webhook(url=f"{WEBHOOK_URL}/api/telegram")
        print(f"--- Telegram webhook set successfully. ---")
    else:
        print("--- WARNING: WEBHOOK_URL not set, skipping webhook setup. ---")
    sys.stdout.flush()

@app.on_event("shutdown")
async def shutdown_event():
    if WEBHOOK_URL:
        await ptb_app.bot.delete_webhook()

@app.post("/api/telegram")
async def telegram_webhook(request: Request):
    update_data = await request.json()
    update = telegram.Update.de_json(update_data, ptb_app.bot)
    await ptb_app.process_update(update)
    return Response(status_code=200)

@app.post("/api/chapa/webhook")
async def chapa_webhook(request: Request):
    payload = await request.json()
    tx_ref = payload.get("tx_ref")
    if payload.get("status") == "success" and tx_ref:
        verification_data = await verify_payment(tx_ref)
        if verification_data and verification_data.get("status") == "success":
            async with async_session() as session:
                async with session.begin():
                    tx = await session.query(Transaction).filter_by(tx_ref=tx_ref).first()
                    if tx and tx.status == 'pending':
                        tx.status = 'completed'
                        user = await session.query(User).filter_by(telegram_id=tx.user_id).first()
                        if user:
                            user.balance += decimal.Decimal(tx.amount)
                            await ptb_app.bot.send_message(
                                chat_id=user.telegram_id,
                                text=f"✅ Your deposit of {tx.amount} ETB has been confirmed."
                            )
                        await session.commit()
    return Response(status_code=200)

@app.get("/health")
def health_check():
    return {"status": "ok"}

print("--- STEP 9: Reached end of api/main.py file. Gunicorn will now take over. ---")
sys.stdout.flush()```

**Step 2: Commit the Change**

Scroll to the bottom of the page and commit the change to your `main` branch. This will trigger a new deployment.

**Step 3: Analyze the New Logs**

Go to the logs for this new deployment on Render. Now, you will see our `--- STEP X ---` messages printed out.

*   If the log stops after **STEP 4** and you see "FATAL ERROR", it means the `TELEGRAM_BOT_TOKEN` is definitely not being set correctly in Render's environment.
*   If the log stops at any other step, it tells us exactly which line of code is causing the crash.

Please share a screenshot of the logs containing these new `--- STEP ---` messages. This will give us the final clue we need.