from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from nanoid import generate  # type: ignore

from src.domain.user.dto import UserOut


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


@dataclass(repr=True, eq=False)
class JobStore(Base): ...


@dataclass(repr=True, eq=False)
class User(Base):
    phone: str = field(default="")
    email: str = field(default="")
    password: str = field(default="")

    @classmethod
    def create(cls, phone: str, email: str, password: str, hasher: PasswordHasher) -> "User":
        return cls(phone=phone, email=email, password=hasher.hash(password))

    def verify(self, password: str, hasher: PasswordHasher) -> bool:
        try:
            return hasher.verify(hash=self.password, password=password)
        except VerifyMismatchError:
            return False

    def to_dto(self):
        return UserOut(
            id=self.id,
            create_date=self.create_date,
            update_date=self.update_date,
            email=self.email,
            phone=self.phone,
        )
