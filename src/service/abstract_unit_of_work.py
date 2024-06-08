import abc
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.abstract_repository import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    async def __aenter__(self) -> "AbstractUnitOfWork":
        self.session: AsyncSession
        self.users: AbstractRepository
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

    @abc.abstractmethod
    def collect_new_events(self):
        raise NotImplementedError
