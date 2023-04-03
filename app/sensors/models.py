from pydantic import BaseModel


class SensorModel(BaseModel):
    id: int
    name: str
    description: str
    location: str
    public_key: str


class CreateSensorModel(BaseModel):
    name: str
    description: str
    location: str
    public_key: str


class UpdateSensorModel(BaseModel):
    name: str
    description: str
    location: str
    public_key: str


class DeleteSensorModel(BaseModel):
    id: int
