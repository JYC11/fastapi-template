from datetime import datetime

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: str
    create_date: datetime
    update_date: datetime | None
    phone: str
    email: str


class UserSearchParams(BaseModel):
    phone: str | None = Field(None)
    email: str | None = Field(None)
