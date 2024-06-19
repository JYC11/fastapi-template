import abc
from typing import Any

from src.service.abstract_view import AbstractView


class AbstractQueryService(abc.ABC):
    def __init__(
        self,
        view: AbstractView,
    ):
        self.view = view

    @abc.abstractmethod
    async def get_one(self, ident: Any) -> Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_one_or_raise(self, ident: Any) -> Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self, *args, **kwargs) -> Any | None:
        raise NotImplementedError
