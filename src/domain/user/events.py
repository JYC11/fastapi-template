from src.domain import Event


class UserCreated(Event):
    id: str


class UserUpdated(Event):
    id: str


class UserDeleted(Event):
    id: str
