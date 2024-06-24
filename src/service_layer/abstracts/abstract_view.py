import abc
from typing import Any, Type

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

    async def get_count(self, query: Any, filters: list) -> int:
        return await self._get_count(query=query, filters=filters)

    async def paginate(
        self,
        query: Select,
        filters: list[Any],
        ordering: list[Any],
        offset: int,
        size: int,
        scalars: bool,
    ):
        return await self._paginate(
            query=query,
            filters=filters,
            ordering=ordering,
            offset=offset,
            size=size,
            scalars=scalars,
        )

    @abc.abstractmethod
    async def _execute(self, query: str | Select, scalars: bool, one: bool):
        raise NotImplementedError

    @abc.abstractmethod
    async def _paginate(
        self,
        query: Select,
        filters: list,
        ordering: list,
        offset: int,
        size: int,
        scalars: bool,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_count(self, query: Select, filters: list[Any]):
        raise NotImplementedError
