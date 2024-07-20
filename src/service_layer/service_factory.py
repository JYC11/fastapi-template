from argon2 import PasswordHasher  # type: ignore

from src.service_layer import unit_of_work, view
from src.service_layer.user.authentication_service import AuthenticationService
from src.service_layer.user.query_service import UserQueryService
from src.service_layer.user.repository import UserRepository


def get_user_query_service() -> UserQueryService:
    return UserQueryService(view=view.get_view(repositories=dict(user=UserRepository)))


def get_auth_service() -> AuthenticationService:
    return AuthenticationService(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
        hasher=PasswordHasher(),
    )
