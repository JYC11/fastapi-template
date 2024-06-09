from datetime import datetime
from typing import Any, Literal

from attrs import define, field
from nanoid import generate  # type: ignore


@define(kw_only=True)
class Base:
    id: str = field(default=generate())
    created_date: datetime = field(default=datetime.now())
    updated_date: datetime | None = field(default=None)

    def __eq__(self, other):
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update(self, data: dict[str, Any]):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self


@define(kw_only=True)
class FailedMessageLog(Base):
    message_type: Literal["COMMAND", "EVENT"] = field()
    message_name: str = field()
    error_message: str = field()


@define(kw_only=True)
class JobStore(Base): ...


@define(kw_only=True)
class User(Base):
    phone: str = field()
    email: str = field()
    password: str = field()
