from pydantic import BaseModel


class MeasureModel(BaseModel):
    id: int
    temperature: float
    humidity: float
    measure_time: int
    sensor_id: int


class CreateMeasureModel(BaseModel):
    temperature: float
    humidity: float
    measure_time: int


class DeleteMeasureModel(BaseModel):
    id: int
