from argon2 import PasswordHasher

from src.service import unit_of_work
from src.service.abstract_service import AbstractService
from src.service.user.repository import UserRepository
from src.service.user.service import UserService


def get_user_service() -> AbstractService:
    return UserService(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
        hasher=PasswordHasher(),
    )
