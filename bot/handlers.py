from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application
from database_models.models import User, Game, Transaction, async_session
from bot.chapa_service import initialize_payment
import decimal

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    async with async_session() as session:
        async with session.begin():
            db_user = await session.get(User, user.id)
            if not db_user:
                db_user = User(telegram_id=user.id, username=user.username)
                session.add(db_user)
                await session.commit()
                await update.message.reply_text(f"Welcome, {user.first_name}! Your Yeab Game Zone account is created.")
            else:
                await update.message.reply_text(f"Welcome back, {user.first_name}!")
    
    await update.message.reply_text(
        "Here's what you can do:\n"
        "/play - Start a new Ludo game\n"
        "/deposit - Add funds to your wallet\n"
        "/withdraw - Request a withdrawal\n"
        "/balance - Check your balance"
    )

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount_str = context.args[0]
        amount = decimal.Decimal(amount_str)
        if amount < 20:
            await update.message.reply_text("Minimum deposit amount is 20 ETB.")
            return
        
        user = update.effective_user
        checkout_url, tx_ref = await initialize_payment(float(amount), user.id, user.first_name)
        
        if checkout_url and tx_ref:
            # Save the pending transaction to the DB
            async with async_session() as session:
                async with session.begin():
                    new_tx = Transaction(user_id=user.id, tx_ref=tx_ref, amount=amount, type='deposit', status='pending')
                    session.add(new_tx)
                    await session.commit()
            
            keyboard = [[InlineKeyboardButton("Click here to Pay", url=checkout_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"To deposit {amount} ETB, please complete the payment using the button below.",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("Sorry, we couldn't create a payment link right now. Please try again later.")
            
    except (IndexError, ValueError):
        await update.message.reply_text("Please specify a valid amount. Usage: /deposit 50")