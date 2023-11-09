import pytest

from quizbot.models import Question


def question(data: dict) -> Question:
    return Question(
        category=data.get("category"),
        type=data.get("type"),
        difficulty=data.get("difficulty"),
        question=data.get("question"),
        correct_answer=data.get("correct_answer"),
        incorrect_answers=data.get("incorrect_answers"),
    )


@pytest.mark.parametrize(
    "create_question",
    [
        question,
        Question.from_dict,
    ],
)
def test_can_create_question(create_question, question_dict) -> None:
    question = create_question(question_dict)

    assert question.category == "Entertainment: Video Games"
    assert question.type == "multiple"
    assert question.difficulty == "easy"
    assert question.question == "Rocket League is a game which features.."
    assert question.correct_answer == "Cars"
    assert question.incorrect_answers == ["Helicopters", "Planes", "Submarines"]
    assert type(question.answers) == tuple
    assert len(question.answers) == 4


@pytest.mark.usefixtures("seed_random")
def test_answer_index(question_dict) -> None:
    question = Question.from_dict(question_dict)

    assert type(question.answer_index) == int
    assert question.answer_index == 1
