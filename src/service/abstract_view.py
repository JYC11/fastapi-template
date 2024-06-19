import abc
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Select

from src.adapters.abstract_repository import AbstractRepository


class AbstractView(abc.ABC):
    user: AbstractRepository
    failed_message_log: AbstractRepository

    async def __aenter__(self) -> "AbstractView":
        self.session: AsyncSession
        self.session_factory: sessionmaker
        self.repositories: dict[str, Type[AbstractRepository]]
        return self

    async def __aexit__(self, *args):
        raise NotImplementedError

    async def execute(self, query: str | Select, scalars: bool, one: bool):
        return await self._execute(
            query=query,
            scalars=scalars,
            one=one,
        )

    @abc.abstractmethod
    async def _execute(self, query: str | Select, scalars: bool, one: bool):
        raise NotImplementedError
