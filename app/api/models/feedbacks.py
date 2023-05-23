from pydantic import BaseModel


class FeedbackBase(BaseModel):
    message: str
    timestamp: int


class Feedback(FeedbackBase):
    id: str
    owner_id: str


class FeedbackCreate(FeedbackBase):
    pass
