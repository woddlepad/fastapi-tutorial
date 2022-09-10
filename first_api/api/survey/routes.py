from datetime import datetime
from typing import Dict, List
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel, Field

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


class AnswerInDB(ClassInDB):
    name: str
    answer_date: datetime = Field(default_factory=datetime.now)
    question_id: str
    answer_id: str


class AnswerQuestionsForm(BaseModel):
    name: str
    answers: Dict[str, str]


class SurveyEvaluationResult(BaseModel):
    name: str
    score: float
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


@router.get("/", response_model=List[QuestionInDB])
def get_questions():
    return QuestionInDB.read_all()


@router.post("/answer")
def answer_survey(
    form_data: AnswerQuestionsForm,
):
    real_answers = []
    for question_id, answer_id in form_data.answers.items():
        question = QuestionInDB.read(question_id)
        real_answers.append(next((a for a in question.answers if a.id == answer_id)))

        answer = AnswerInDB(
            id=f"{form_data.name}-{question_id}-{datetime.now()}",
            name=form_data.name,
            question_id=question_id,
            answer_id=answer_id,
        )
        answer.save(overwrite=True)
    return SurveyEvaluationResult(
        name=form_data.name,
        score=sum(a.value for a in real_answers),
        answers=real_answers,
    )
