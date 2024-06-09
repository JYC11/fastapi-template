from typing import Union

from src.domain.command import Command
from src.domain.event import Event

Message = Union[Command, Event]
