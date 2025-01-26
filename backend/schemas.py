# schemas.py
from pydantic import BaseModel

class Query(BaseModel):
    question: str
    course_id: int

class Answer(BaseModel):
    answer: str
