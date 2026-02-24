from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    tokens: int
    prompt_tokens: int
    completion_tokens: int
    cost: float
