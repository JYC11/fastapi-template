import abc
from collections import deque
from typing import Any

from src.domain import Message
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork


class CommandHandler(abc.ABC):
    uow: AbstractUnitOfWork

    @abc.abstractmethod
    async def execute(self, cmd) -> Any: ...

    @property
    def events(self) -> deque[Message]:
        return self.uow.events
