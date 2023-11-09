from dataclasses import dataclass, field
from random import shuffle


@dataclass(frozen=True)
class Question:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
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
