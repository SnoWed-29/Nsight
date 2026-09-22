from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    sql: str
    columns: list[str]
    rows: list[list]
    count: int
    answer: str