from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from nanoid import generate  # type: ignore


@dataclass(repr=True, eq=False)
class Base:
    id: str = field(default_factory=generate)
    create_date: datetime = field(init=False, repr=True)
    update_date: datetime = field(init=False, repr=True)

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


@dataclass(repr=True, eq=False)
class FailedMessageLog(Base):
    message_type: Literal["COMMAND", "EVENT"] = field(default="EVENT")
    message_name: str = field(default="")
    error_message: str = field(default="")


@dataclass(repr=True, eq=False)
class JobStore(Base): ...


@dataclass(repr=True, eq=False)
class User(Base):
    phone: str = field(default="")
    email: str = field(default="")
    password: str = field(default="")
