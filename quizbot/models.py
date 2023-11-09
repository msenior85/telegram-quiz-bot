<<<<<<< HEAD:quizbot/models.py
from dataclasses import dataclass, field
from random import shuffle


@dataclass(frozen=True)
=======
from dataclasses import dataclass
from random import shuffle


@dataclass
>>>>>>> 733ff08 (Created Question model):bot/models.py
class Question:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
<<<<<<< HEAD:quizbot/models.py
    incorrect_answers: list[str]
    answers: tuple[str] = field(init=False, default=None)

    def __post_init__(self):
        if self.answers is None:
            all_answers = list(self.incorrect_answers)
            all_answers.append(self.correct_answer)
            shuffle(all_answers)
            object.__setattr__(self, "answers", tuple(all_answers))

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @property
    def answer_index(self) -> int:
        return self.answers.index(self.correct_answer)
=======
    incorrect_answers: list(str)

    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data.get("category"),
            type=data.get("type"),
            difficulty=data.get("difficulty"),
            question=data.get("question"),
            correct_answer=data.get("correct_answer"),
            incorrect_answers=data.get("incorrect_answer"),
        )

    @property
    def answers(self):
        all_answers = self.incorrect_answers.extend(self.correct_answer)
        return shuffle(all_answers)
>>>>>>> 733ff08 (Created Question model):bot/models.py
