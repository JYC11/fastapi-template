from pydantic import BaseModel, Field

from src.domain.user.dto import UserOut
from src.entrypoints.dto import PaginationOut


class UserCreateIn(BaseModel):
    email: str = Field(...)
    phone: str = Field(...)
    password: str = Field(...)


class UserUpdateIn(BaseModel):
    email: str = Field(...)
    phone: str = Field(...)


class UserPaginatedOut(PaginationOut):
    items: list[UserOut] = Field(...)
