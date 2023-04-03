from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool


class UpdateUserModel(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool


class DeleteUserModel(BaseModel):
    id: int
