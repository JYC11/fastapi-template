import abc
from collections import deque
from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.abstract_repository import AbstractRepository
from src.domain import Message


class AbstractUnitOfWork(abc.ABC):
    async def __aenter__(self) -> "AbstractUnitOfWork":
        self.session: AsyncSession
        self.repositories: dict[str, Type[AbstractRepository]]
        self.events: deque[Message]
        self.users: AbstractRepository
        self.failed_message_log: AbstractRepository
        return self

    async def __aexit__(self, *args):
        raise NotImplementedError

    async def commit(self):
        await self._commit()

    async def rollback(self):
        await self._rollback()

    async def refresh(self, object: Any):
        await self._refresh(object)

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _refresh(self, object: Any):
        raise NotImplementedError
