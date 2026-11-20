"""Telegram Bot Starter — a clean template built on python-telegram-bot v21.

Setup:
  1. Copy .env.example to .env and fill in BOT_TOKEN (from @BotFather).
  2. pip install -r requirements.txt
  3. python bot.py
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
try:
    ADMIN_ID = int(os.environ.get("ADMIN_ID", "0") or 0)
except ValueError:
    raise SystemExit(
        "ADMIN_ID must be a numeric Telegram user ID. "
        "Check your .env file (get your ID from @userinfobot)."
    ) from None

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Conversation states
FEEDBACK = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to /start."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! I am a bot built with the Telegram Bot Starter template.\n\n"
        "Try /help to see what I can do."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to /help."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Say hello\n"
        "/help - Show this help\n"
        "/feedback - Send feedback to the admin\n"
        "/broadcast <message> - Admin only: send a message to all users (demo: replies to you)"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo back any plain text message."""
    await update.message.reply_text(f"You said: {update.message.text}")


async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the /feedback conversation."""
    await update.message.reply_text("Please type your feedback (or /cancel to stop).")
    return FEEDBACK


async def feedback_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive the feedback text and finish the conversation."""
    text = update.message.text
    logger.info("Feedback from %s: %s", update.effective_user.id, text)
    forwarded = False
    if ADMIN_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"New feedback from {update.effective_user.full_name}:\n{text}",
            )
            forwarded = True
        except Exception as exc:  # noqa: BLE001 - log and continue
            logger.warning("Could not forward feedback to admin: %s", exc)
    if forwarded:
        await update.message.reply_text("Thanks! Your feedback has been sent.")
    else:
        # No admin configured, or forwarding failed: don't claim it was sent.
        await update.message.reply_text("Thanks! Your feedback has been recorded.")
    return ConversationHandler.END


async def feedback_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the /feedback conversation."""
    await update.message.reply_text("Feedback cancelled.")
    return ConversationHandler.END


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin-only /broadcast. Demo version: confirms the message instead of sending."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Sorry, only the admin can use /broadcast.")
        return
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    # In a real bot, loop over stored user IDs and send the message.
    await update.message.reply_text(f"Broadcast ready to send to all users:\n{text}")


def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is missing. Copy .env.example to .env and fill it in.")
    app = Application.builder().token(BOT_TOKEN).build()

    feedback = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback_start)],
        states={FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_received)]},
        fallbacks=[CommandHandler("cancel", feedback_cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(feedback)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
