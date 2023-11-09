from unittest.mock import AsyncMock, Mock, patch

import pytest

from quizbot.api import QuizBotError, get_questions
from quizbot.models import Question


@patch("quizbot.api.AsyncClient")
@pytest.mark.asyncio
async def test_get_questions(mock_async_client, question_dict):
    # Mock the behavior of the AsyncClient
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": [question_dict]}
    mock_async_client.get = AsyncMock()
    # mock_async_client.get.return_value = mock_response
    mock_async_client.return_value.__aenter__.return_value.get.return_value = (
        mock_response
    )

    # Call the function
    questions = await get_questions(1)

    # Assertions
    assert len(questions) == 1
    question = questions[0]
    assert isinstance(question, Question)
    assert question.question == "Rocket League is a game which features.."
    assert question.correct_answer == "Cars"
    assert question.incorrect_answers == ["Helicopters", "Planes", "Submarines"]

    # Mock response error
    mock_response.json.return_value = ValueError
    with pytest.raises(QuizBotError):
        await get_questions(1)

    # Mock non succesful status code
    mock_response.status_code = 500
    questions = await get_questions(5)
    assert len(questions) == 0
