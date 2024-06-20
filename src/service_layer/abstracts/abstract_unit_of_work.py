import abc
from collections import deque
from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.adapters.abstract_repository import AbstractRepository
from src.domain import Message


class AbstractUnitOfWork(abc.ABC):
    user: AbstractRepository
    failed_message_log: AbstractRepository

    async def __aenter__(self) -> "AbstractUnitOfWork":
        self.session: AsyncSession
        self.session_factory: sessionmaker
        self.repositories: dict[str, Type[AbstractRepository]]
        self.events: deque[Message] = deque()
        return self

    async def __aexit__(self, *args):
        raise NotImplementedError

    async def commit(self):
        await self._commit()

    async def flush(self):
        await self._flush()

    async def rollback(self):
        await self._rollback()

    async def refresh(self, object: Any):
        await self._refresh(object)

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _flush(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _refresh(self, object: Any):
        raise NotImplementedError
