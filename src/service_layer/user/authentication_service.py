from typing import Literal

from argon2 import PasswordHasher

from src.common.security import token
from src.domain.user.model import User
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.exceptions import Forbidden, Unauthorized
from src.utils.log_utils import logging_decorator

LOG_PATH = "src.service_layer.user.command_service.AuthService"


class AuthenticationService:

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        hasher: PasswordHasher,
    ):
        self.uow = uow
        self.hasher = hasher

    @logging_decorator(LOG_PATH)
    async def login(self, email: str, password: str) -> tuple[str, str]:
        async with self.uow:
            user: User | None = await self.uow.user.get_by(email__eq=email)
            if not user:
                raise Unauthorized("email of password is incorrect")

            if not user.verify(password=password, hasher=self.hasher):
                raise Unauthorized("email of password is incorrect")

            if self.hasher.check_needs_rehash(hash=user.password):
                user.update_password(password=password, hasher=self.hasher)
                await self.uow.commit()

            private_claims = {"email": user.email, "phone": user.phone}

            access_token = token.create_jwt_token(
                subject=user.id,
                private_claims=private_claims,
                refresh=False,
            )

            refresh_token = token.create_jwt_token(
                subject=user.id,
                private_claims=private_claims,
                refresh=True,
            )

            return access_token, refresh_token

    @logging_decorator(LOG_PATH)
    async def refresh(self, refresh_token: str, grant_type: Literal["refresh_token"]):
        async with self.uow:
            if grant_type != "refresh_token":
                raise Forbidden("incorrect grant type")

            try:
                decoded: token.Token = token.validate_jwt_token(token=refresh_token)
            except token.TokenExpired as e:
                raise Forbidden(str(e))
            except token.InvalidToken as e:
                raise Forbidden(str(e))

            id = decoded.sub
            user: User | None = await self.uow.user.get(ident=id)
            if not user:
                raise Forbidden(f"user with {id} not found")

            return token.create_jwt_token(
                subject=user.id,
                private_claims={
                    "email": user.email,
                    "phone": user.phone,
                },
                refresh=False,
            )
