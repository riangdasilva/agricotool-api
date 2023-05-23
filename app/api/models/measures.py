from pydantic import BaseModel


class MeasureBase(BaseModel):
    temperature: float
    humidity: float
    timestamp: int


class Measure(MeasureBase):
    id: str
    owner_id: str


class MeasureCreate(MeasureBase):
    api_key: str
    pass
