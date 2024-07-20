from dataclasses import dataclass, field

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.domain.base import Base
from src.domain.user.dto import UserOut
from src.domain.user.enums import FeatureAuthorizations, UserType


@dataclass(repr=True, eq=False)
class User(Base):
    phone: str = field(default="")
    email: str = field(default="")
    password: str = field(default="")
    type: str = field(default=UserType.NORMAL.value)
    authorized_features: list["AuthorizedFeatures"] = field(default_factory=list)

    @classmethod
    def create(cls, phone: str, email: str, password: str, hasher: PasswordHasher) -> "User":
        return cls(phone=phone, email=email, password=hasher.hash(password=password))

    def verify(self, password: str, hasher: PasswordHasher) -> bool:
        try:
            return hasher.verify(hash=self.password, password=password)
        except VerifyMismatchError:
            return False

    def update_password(self, password: str, hasher: PasswordHasher):
        self.password = hasher.hash(password=password)

    def to_dto(self):
        return UserOut(
            id=self.id,
            create_date=self.create_date,
            update_date=self.update_date,
            email=self.email,
            phone=self.phone,
        )


@dataclass(repr=True, eq=False)
class AuthorizedFeatures(Base):
    user_id: str = field(default="")
    user: User = field(init=False)
    feature: str = field(default=FeatureAuthorizations.NONE.value)
