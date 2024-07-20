import abc
from typing import Any

from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork


class EventHandler(abc.ABC):
    uow: AbstractUnitOfWork

    @abc.abstractmethod
    async def execute(self, event) -> Any: ...
