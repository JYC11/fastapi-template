from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from nanoid import generate  # type: ignore


@dataclass(repr=True, eq=False)
class Base:
    id: str = field(default_factory=generate)
    create_date: datetime = field(default_factory=datetime.now, repr=True)
    update_date: datetime | None = field(default=None, repr=True)

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

    def to_dto(self):
        raise NotImplementedError


@dataclass(repr=True, eq=False)
class FailedMessageLog(Base):
    message_type: Literal["COMMAND", "EVENT"] = field(default="EVENT")
    message_name: str = field(default="")
    error_message: str = field(default="")
