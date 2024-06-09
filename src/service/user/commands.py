from src.domain.command import Command


class CreateUser(Command):
    phone: str
    email: str
    password: str


class UpdateUser(Command):
    id: str
    phone: str
    email: str


# TODO update password


class DeleteUser(Command):
    id: str
