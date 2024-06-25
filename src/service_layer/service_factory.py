from argon2 import PasswordHasher  # type: ignore

from src.service_layer import unit_of_work, view
from src.service_layer.abstracts.abstract_query_service import AbstractQueryService
from src.service_layer.abstracts.abstract_service import AbstractService
from src.service_layer.user.command_service import UserCommandService
from src.service_layer.user.query_service import UserQueryService
from src.service_layer.user.repository import UserRepository


def get_user_command_service() -> AbstractService:
    return UserCommandService(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
        hasher=PasswordHasher(),
    )


def get_user_query_service() -> AbstractQueryService:
    return UserQueryService(view=view.get_view(repositories=dict(user=UserRepository)))
