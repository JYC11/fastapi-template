from typing import Type

from src.adapters.abstract_repository import AbstractRepository
from src.service.abstract_unit_of_work import AbstractUnitOfWork
from src.service.unit_of_work import SqlAlchemyUnitOfWork
from src.service.user.repository import UserRepository
from src.service.user.service import UserService


class ServiceFactory:
    @staticmethod
    def get_unit_of_work(repositories: dict[str, Type[AbstractRepository]]) -> AbstractUnitOfWork:
        return SqlAlchemyUnitOfWork(repositories=repositories)

    @classmethod
    def get_user_service(cls) -> UserService:
        uow = cls.get_unit_of_work(repositories=dict(user=UserRepository))
        return UserService(uow=uow)
