from typing import Union

from pydantic import BaseModel


class Command(BaseModel): ...


class Event(BaseModel): ...


Message = Union[Command, Event]
