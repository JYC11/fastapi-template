from argon2 import PasswordHasher

from src.service import unit_of_work, view
from src.service.abstract_query_service import AbstractQueryService
from src.service.abstract_service import AbstractService
from src.service.user.query_service import UserQueryService
from src.service.user.repository import UserRepository
from src.service.user.service import UserService


def get_user_service() -> AbstractService:
    return UserService(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
        hasher=PasswordHasher(),
    )


def get_user_view() -> AbstractQueryService:
    return UserQueryService(view=view.get_view(repositories=dict(user=UserRepository)))
