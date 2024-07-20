from argon2 import PasswordHasher  # type: ignore

from src.service_layer import unit_of_work
from src.service_layer.abstracts.abstract_command_handler import CommandHandler
from src.service_layer.user.command_handlers import UserCreationHandler, UserDeleteHandler, UserUpdateHandler
from src.service_layer.user.repository import UserRepository


def get_user_creation_handler() -> CommandHandler:
    return UserCreationHandler(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
        hasher=PasswordHasher(),
    )


def get_user_update_handler() -> CommandHandler:
    return UserUpdateHandler(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
    )


def get_user_delete_handler() -> CommandHandler:
    return UserDeleteHandler(
        uow=unit_of_work.get_uow(repositories=dict(user=UserRepository)),
    )
