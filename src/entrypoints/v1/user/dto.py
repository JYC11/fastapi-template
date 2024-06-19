from pydantic import BaseModel, Field


class UserCreateIn(BaseModel):
    email: str = Field(...)
    phone: str = Field(...)
    password: str = Field(...)


class UserUpdateIn(BaseModel):
    email: str = Field(...)
    phone: str = Field(...)
