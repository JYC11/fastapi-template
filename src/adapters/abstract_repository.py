import abc
from typing import Any


class AbstractRepository(abc.ABC):
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

    async def get_all(self, *args, **kwargs):
        return await self._get_all(*args, **kwargs)

    @abc.abstractmethod
    def _add(self, item: Any) -> None: ...

    @abc.abstractmethod
    def _add_all(self, items: list) -> None: ...

    @abc.abstractmethod
    async def _get(self, ident: Any) -> Any | None: ...

    @abc.abstractmethod
    async def _get_by(self, *args, **kwargs) -> Any | None: ...

    @abc.abstractmethod
    async def _remove(self, ident: Any) -> None: ...

    @abc.abstractmethod
    async def _get_all(self, *args, **kwargs) -> list[Any]: ...
