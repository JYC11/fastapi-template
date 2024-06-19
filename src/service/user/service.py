import asyncio

from argon2 import PasswordHasher

from src.domain.models import User
from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.events import UserCreated, UserDeleted, UserUpdated
from src.service.abstracts.abstract_service import AbstractService
from src.service.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service.exceptions import ItemNotFound
from src.service.user.exceptions import DuplicateUserByEmail, DuplicateUserByPhone


class UserService(AbstractService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        hasher: PasswordHasher,
    ):
        self.uow = uow
        self.hasher = hasher

    async def create(self, cmd: CreateUser) -> User:
        async with self.uow:
            duplicate_user_by_email, duplicate_user_by_phone = await asyncio.gather(
                self.uow.user.get_by(email__eq=cmd.email),
                self.uow.user.get_by(phone__eq=cmd.phone),
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
            self.uow.user.add(user)
            await self.uow.commit()
            self.uow.events.append(UserCreated(id=user.id))
            return user

    async def update(self, cmd: UpdateUser) -> User:
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
            self.uow.events.append(UserUpdated(id=user.id))
            return user

    async def delete(self, cmd: DeleteUser) -> None:
        async with self.uow:
            await self.uow.user.remove(ident=cmd.id)
            await self.uow.commit()
            self.uow.events.append(UserDeleted(id=cmd.id))
            return
