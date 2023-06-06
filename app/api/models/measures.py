from pydantic import BaseModel


class MeasureBase(BaseModel):
    temperature: float
    humidity: float


class Measure(MeasureBase):
    id: str
    owner_id: str
    timestamp: int


class MeasureCreate(MeasureBase):
    api_key: str
    pass
