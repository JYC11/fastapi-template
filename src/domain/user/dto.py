from datetime import datetime

from pydantic import BaseModel


class UserOut(BaseModel):
    id: str
    create_date: datetime
    update_date: datetime | None
    phone: str
    email: str


class UserSearchParams(BaseModel):
    phone: str | None
    email: str | None
