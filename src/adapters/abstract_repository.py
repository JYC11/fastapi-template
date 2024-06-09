import abc
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(abc.ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession

    @abc.abstractmethod
    def _add(self, item: Any) -> None: ...

    @abc.abstractmethod
    def _add_all(self, items: list[Any]) -> None: ...

    @abc.abstractmethod
    async def _get(self, ident: Any) -> Any | None: ...

    @abc.abstractmethod
    async def _get_by(self, *args, **kwargs) -> Any | None: ...

    @abc.abstractmethod
    async def _remove(self, ident: Any) -> None: ...

    @abc.abstractmethod
    async def _list(self, *args, **kwargs) -> list[Any]: ...

    def add(self, item: Any):
        self._add(item)

    def add_all(self, items: list[Any]):
        self._add_all(items)

    async def get(self, ident: Any):
        return await self._get(ident)

    async def get_by(self, *args, **kwargs):
        return await self._get_by(*args, **kwargs)

    async def remove(self, ident: Any):
        return await self._remove(ident)

    async def list(self, *args, **kwargs):
        return await self._list(*args, **kwargs)
