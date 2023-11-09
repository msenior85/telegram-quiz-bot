import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    PicklePersistence,
    PollHandler,
    filters,
)

from quizbot.handlers import help_command, quiz, receive_quiz_answer, start

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    # load environment variables from .env file
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    # persistence to store bot data on restarts
    persistence = PicklePersistence(filepath=".bot_data")
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("question", quiz))
    application.add_handler(CallbackQueryHandler(quiz, "next"))
    application.add_handler(PollHandler(receive_quiz_answer))
    application.add_handler(MessageHandler(filters.COMMAND, help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
