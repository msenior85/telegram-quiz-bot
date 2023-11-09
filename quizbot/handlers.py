import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll, Update
from telegram.ext import ContextTypes

from quizbot import api

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.first_name}, please send /quiz to start a new quiz or /question to get one question."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Please send /quiz to start a new quiz or /question to get one question."
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a quiz poll with one question"""
    questions = await api.get_questions()
    question = questions[0]

    if update.callback_query:
        await update.callback_query.edit_message_reply_markup()

    message = await update.effective_message.reply_poll(
        question.question,
        question.answers,
        type=Poll.QUIZ,
        correct_option_id=question.answer_index,
    )
    # data to be used in receive_quiz_answer
    payload = {
        message.poll.id: {
            "chat_id": update.effective_chat.id,
            "message_id": message.message_id,
        }
    }
    context.bot_data.update(payload)


async def receive_quiz_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    quiz_data = context.bot_data.get(update.poll.id)
    chat_id = quiz_data.get("chat_id")
    message_id = quiz_data.get("message_id")

    chosen_answer = None
    for i, option in enumerate(update.poll.options):
        if option.voter_count == 1:
            chosen_answer = i
            break

    if chosen_answer == update.poll.correct_option_id:
        logger.info("Correct answer chosen.")

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Next Question", callback_data="next")]]
    )

    if quiz_data and not update.poll.is_closed:
        await context.bot.stop_poll(chat_id, message_id, reply_markup=reply_markup)
