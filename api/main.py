import os
import asyncio
import telegram
from fastapi import FastAPI, Request, Response
from telegram.ext import Application
from dotenv import load_dotenv
from bot.handlers import start, deposit # Import all your handlers
from bot.chapa_service import verify_payment
from database_models.models import User, Transaction, async_session
import decimal

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# --- FastAPI App Setup ---
app = FastAPI()
ptb_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

@app.on_event("startup")
async def startup_event():
    # Register handlers
    ptb_app.add_handler(telegram.ext.CommandHandler("start", start))
    ptb_app.add_handler(telegram.ext.CommandHandler("deposit", deposit))
    # ... add other handlers (CallbackQueryHandler, etc.)

    # Set webhook
    if WEBHOOK_URL:
        await ptb_app.bot.set_webhook(url=f"{WEBHOOK_URL}/api/telegram")
        print(f"Telegram webhook set to {WEBHOOK_URL}/api/telegram")
    else:
        print("WEBHOOK_URL not set, skipping webhook setup.")


@app.on_event("shutdown")
async def shutdown_event():
    if WEBHOOK_URL:
        await ptb_app.bot.delete_webhook()
        print("Telegram webhook deleted.")

@app.post("/api/telegram")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates."""
    update_data = await request.json()
    update = telegram.Update.de_json(update_data, ptb_app.bot)
    await ptb_app.process_update(update)
    return Response(status_code=200)

@app.post("/api/chapa/webhook")
async def chapa_webhook(request: Request):
    """Handle incoming Chapa payment notifications."""
    payload = await request.json()
    print(f"Received Chapa webhook: {payload}")

    # For security, always verify the transaction with Chapa's API
    tx_ref = payload.get("tx_ref")
    if payload.get("status") == "success" and tx_ref:
        verification_data = await verify_payment(tx_ref)
        if verification_data and verification_data.get("status") == "success":
            # Update database
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
                                text=f"✅ Your deposit of {tx.amount} ETB has been confirmed and added to your balance."
                            )
                        await session.commit()
    return Response(status_code=200)

@app.get("/health")
def health_check():
    """Health check endpoint for Render."""
    return {"status": "ok"}