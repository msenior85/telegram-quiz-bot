import random
from unittest.mock import MagicMock

import pytest
from telegram import Update
from telegram.ext import ContextTypes


@pytest.fixture
def question_dict() -> dict:
    return {
        "category": "Entertainment: Video Games",
        "type": "multiple",
        "difficulty": "easy",
        "question": "Rocket League is a game which features..",
        "correct_answer": "Cars",
        "incorrect_answers": ["Helicopters", "Planes", "Submarines"],
    }


@pytest.fixture
def seed_random():
    # Set a fixed seed for the random number generator for testing
    random.seed(123)


@pytest.fixture
def mock_update():
    return MagicMock(spec=Update)


@pytest.fixture
def mock_context():
    return MagicMock(spec=ContextTypes.DEFAULT_TYPE)
