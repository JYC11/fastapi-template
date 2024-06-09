import asyncio

from argon2 import PasswordHasher

from src.domain.models import User
from src.service.abstract_service import AbstractService
from src.service.abstract_unit_of_work import AbstractUnitOfWork
from src.service.exceptions import ItemNotFound
from src.service.user.commands import CreateUser, DeleteUser, UpdateUser
from src.service.user.events import UserCreated, UserDeleted, UserUpdated
from src.service.user.exceptions import DuplicateUserByEmail, DuplicateUserByPhone


class UserService(AbstractService):
    def __init__(self, uow: AbstractUnitOfWork, hasher: PasswordHasher):
        self.uow = uow
        self.hasher = hasher

    async def create(self, cmd: CreateUser) -> User:
        async with self.uow:
            duplicate_user_by_email, duplicate_user_by_phone = await asyncio.gather(
                self.uow.users.get_by(email__eq=cmd.email),
                self.uow.users.get_by(phone__eq=cmd.phone),
            )

            if duplicate_user_by_email:
                raise DuplicateUserByEmail()
            if duplicate_user_by_phone:
                raise DuplicateUserByPhone()

            user = User(
                phone=cmd.phone,
                email=cmd.email,
                password=self.hasher.hash(cmd.password),
            )
            self.uow.users.add(user)
            await self.uow.commit()
            self.uow.events.appendleft(UserCreated())
            return user

    async def update(self, cmd: UpdateUser) -> User:
        async with self.uow:
            user: User | None = await self.uow.users.get(ident=cmd.id)
            if not user:
                raise ItemNotFound()
            user.update(
                data={
                    "email": cmd.email,
                    "phone": cmd.phone,
                }
            )
            await self.uow.commit()
            self.uow.events.appendleft(UserUpdated())
            return user

    async def delete(self, cmd: DeleteUser) -> None:
        async with self.uow:
            await self.uow.users.remove(ident=cmd.id)
            await self.uow.commit()
            self.uow.events.appendleft(UserDeleted())
            return
