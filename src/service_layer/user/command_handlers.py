import asyncio

from argon2 import PasswordHasher

from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.dto import UserOut
from src.domain.user.events import UserCreated, UserDeleted, UserUpdated
from src.domain.user.model import User
from src.service_layer.abstracts.abstract_command_handler import CommandHandler
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.exceptions import DuplicateRecord, ItemNotFound
from src.utils.log_utils import logging_decorator

LOG_PATH = "src.service_layer.user.command_handlers"


class UserCreationHandler(CommandHandler):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        hasher: PasswordHasher,
    ):
        self.uow = uow
        self.hasher = hasher

    @logging_decorator(f"{LOG_PATH}.UserCreationHandler.execute")
    async def execute(self, cmd: CreateUser) -> UserOut:
        async with self.uow:
            duplicate_user_by_email, duplicate_user_by_phone = await asyncio.gather(
                self.uow.user.get_by(email__eq=cmd.email),
                self.uow.user.get_by(phone__eq=cmd.phone),
            )

            if duplicate_user_by_email:
                raise DuplicateRecord("duplicate user by email")
            if duplicate_user_by_phone:
                raise DuplicateRecord("duplicate user by phone")

            user = User.create(
                phone=cmd.phone,
                email=cmd.email,
                password=cmd.password,
                hasher=self.hasher,
            )
            self.uow.user.add(user)
            await self.uow.commit()
            self.uow.events.append(UserCreated(id=user.id))
            return user.to_dto()


class UserUpdateHandler(CommandHandler):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    @logging_decorator(f"{LOG_PATH}.UserUpdateHandler.execute")
    async def execute(self, cmd: UpdateUser) -> UserOut:
        async with self.uow:
            user: User | None = await self.uow.user.get(ident=cmd.id)
            if not user:
                raise ItemNotFound()
            user.update(
                data={
                    "email": cmd.email,
                    "phone": cmd.phone,
                }
            )
            await self.uow.commit()
            await self.uow.refresh(user)
            self.uow.events.append(UserUpdated(id=user.id))
            return user.to_dto()


class UserDeleteHandler(CommandHandler):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    @logging_decorator(f"{LOG_PATH}.UserDeleteHandler.execute")
    async def execute(self, cmd: DeleteUser) -> None:
        async with self.uow:
            await self.uow.user.remove(ident=cmd.id)
            await self.uow.commit()
            self.uow.events.append(UserDeleted(id=cmd.id))
            return
