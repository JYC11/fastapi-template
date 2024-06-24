import abc
from typing import Any

from src.entrypoints.dto import PaginationParams
from src.service_layer.abstracts.abstract_view import AbstractView


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
    async def paginate(self, req: Any, pagination_params: PaginationParams) -> Any | None:
        raise NotImplementedError
