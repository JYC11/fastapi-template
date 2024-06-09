from typing import Type

from argon2 import PasswordHasher

from src.adapters.abstract_repository import AbstractRepository
from src.service.abstract_service import AbstractService
from src.service.abstract_unit_of_work import AbstractUnitOfWork
from src.service.unit_of_work import SqlAlchemyUnitOfWork
from src.service.user.repository import UserRepository
from src.service.user.service import UserService


def get_unit_of_work(repositories: dict[str, Type[AbstractRepository]]) -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(repositories=repositories)


def get_user_service() -> AbstractService:
    return UserService(
        uow=get_unit_of_work(repositories=dict(user=UserRepository)),
        hasher=PasswordHasher(),
    )
