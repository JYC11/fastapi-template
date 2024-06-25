from typing import Any

from sqlalchemy import select

from src.domain.models import User
from src.domain.user.dto import UserOut, UserSearchParams
from src.entrypoints.dto import PaginationParams
from src.service_layer.abstracts.abstract_query_service import AbstractQueryService
from src.service_layer.abstracts.abstract_view import AbstractView
from src.service_layer.exceptions import ItemNotFound
from src.utils.log_utils import logging_decorator

LOG_PATH = "src.service_layer.user.query_service.UserQueryService"


class UserQueryService(AbstractQueryService):
    def __init__(self, view: AbstractView):
        super().__init__(view)

    @logging_decorator(LOG_PATH)
    async def get_one(self, ident: str) -> UserOut | None:
        async with self.view:
            user: User | None = await self.view.user.get(ident=ident)
            if not user:
                return None
            return user.to_dto()

    @logging_decorator(LOG_PATH)
    async def get_one_or_raise(self, ident: str) -> UserOut:
        async with self.view:
            user: UserOut | None = await self.view.user.get(ident=ident)
            if not user:
                raise ItemNotFound
            return user

    @logging_decorator(LOG_PATH)
    async def paginate(
        self, search_params: UserSearchParams, pagination_params: PaginationParams
    ) -> tuple[list[UserOut], int]:
        async with self.view:
            query = select(User)

            filters: list[Any] = []
            if search_params.phone is not None:
                filters.append(User.email.like(f"%{search_params.phone}%"))  # type: ignore
            if search_params.email is not None:
                filters.append(User.email.like(f"%{search_params.email}%"))  # type: ignore

            total = await self.view.get_count(query=query, filters=filters)
            if total == 0:
                return [], 0

            contours: list[User] = await self.view.paginate(
                query=query,
                filters=filters,
                ordering=pagination_params.get_order_by_conditions(model=User),
                offset=pagination_params.offset,
                size=pagination_params.size,
                scalars=True,
            )

            return [x.to_dto() for x in contours], total
