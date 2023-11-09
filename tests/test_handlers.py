from unittest.mock import AsyncMock, Mock, patch

import pytest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll

from quizbot.handlers import help_command, quiz, receive_quiz_answer, start
from quizbot.models import Question


@pytest.mark.asyncio
async def test_start(mock_update, mock_context):
    mock_update.effective_user.first_name = "John"

    mock_update.message.reply_html = AsyncMock()
    await start(mock_update, mock_context)

    # Check if the message is sent as expected
    mock_update.message.reply_html.assert_called_with(
        "Hi John, please send /quiz to start a new quiz or /question to get one question."
    )


@pytest.mark.asyncio
async def test_help_command(mock_update, mock_context):
    mock_update.message.reply_text = AsyncMock()
    await help_command(mock_update, mock_context)

    # Check if the message is sent as expected
    mock_update.message.reply_text.assert_called_with(
        "Please send /quiz to start a new quiz or /question to get one question."
    )


@patch("quizbot.api.get_questions")
@pytest.mark.asyncio
async def test_quiz(mock_get_questions, mock_update, mock_context, question_dict):
    # Mock the necessary objects
    question = Question.from_dict(question_dict)
    mock_get_questions.return_value = [question]

    mock_update.callback_query.edit_message_reply_markup = AsyncMock()
    mock_update.effective_message.reply_poll = AsyncMock()

    mock_update.effective_message.reply_poll.return_value.poll.id = 123
    mock_update.effective_chat.id = 456

    # Call the function
    await quiz(mock_update, mock_context)

    # Assert that the expected methods were called with the correct arguments
    mock_update.effective_message.reply_poll.assert_called_with(
        question.question,
        question.answers,
        type=Poll.QUIZ,
        correct_option_id=question.answer_index,
    )
    mock_context.bot_data.update.assert_called_with(
        {
            123: {
                "chat_id": 456,
                "message_id": mock_update.effective_message.reply_poll.return_value.message_id,
            }
        }
    )


@pytest.mark.asyncio
async def test_receive_quiz_answer(mock_update, mock_context):
    mock_context.bot.stop_poll = AsyncMock()

    option1 = Mock()
    option1.voter_count = 0
    option2 = Mock()
    option2.voter_count = 1

    mock_update.poll.id = 123
    mock_update.poll.options = [option1, option2]
    mock_update.poll.correct_option_id = 1
    mock_update.poll.is_closed = False
    poll_data = {"chat_id": 456, "message_id": 789}
    mock_context.bot_data = {}
    mock_context.bot_data[123] = poll_data

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Next Question", callback_data="next")]]
    )

    # Call the function under test
    await receive_quiz_answer(mock_update, mock_context)

    # Add your assertions here to check if the function behaves as expected
    mock_context.bot.stop_poll.assert_called_with(
        poll_data["chat_id"],
        poll_data["message_id"],
        reply_markup=reply_markup,
    )
