import logging
from html import unescape

from httpx import AsyncClient

from quizbot.models import Question

logger = logging.getLogger(__name__)

API_URL = "https://opentdb.com/api.php"


class QuizBotError(Exception):
    """Raised when an error is encountered in the get_questions function"""


async def get_questions(number: int = 1) -> list[Question]:
    async with AsyncClient() as http_client:
        try:
            response = await http_client.get(
                API_URL,
                params={
                    "amount": number,
                },
            )
            if response.status_code == 200:
                logger.info("Received successful response from opentdb api!")
                data = response.json()
                questions = []
                for val in data.get("results"):
                    val["question"] = unescape(val.get("question"))
                    questions.append(Question.from_dict(val))
                return questions
            else:
                logger.error(f"Received unsuccessful response from opentdb! {response}")
                return []
        except Exception as e:
            msg = "An error occurred while obtaining questions from opentdb!"
            logger.error(msg, exc_info=e)
            raise QuizBotError(msg)
