from typing import List
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from first_api.db import ClassInDB


router = APIRouter()


class Answer(BaseModel):
    id: str
    value: float
    answer: str


class QuestionInDB(ClassInDB):
    question: str
    answers: List[Answer]


class CreateQuestionForm(BaseModel):
    name: str
    question: str
    answers: List[Answer]


@router.post("/question/create", response_model=QuestionInDB)
def create_question(form_data: CreateQuestionForm):
    question = QuestionInDB(
        id=form_data.name, question=form_data.question, answers=form_data.answers
    )
    try:
        question.save(overwrite=False)
    except ValueError:
        raise HTTPException(
            405,
            f"Question with name {form_data.name} already exists. Choose a different name.",
        )
    return question
