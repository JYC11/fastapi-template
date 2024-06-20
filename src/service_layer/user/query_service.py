from src.domain.models import User
from src.service_layer.abstracts.abstract_query_service import AbstractQueryService
from src.service_layer.abstracts.abstract_view import AbstractView
from src.service_layer.exceptions import ItemNotFound
from src.utils.log_utils import logging_decorator

LOG_PATH = "src.service_layer.user.query_service.UserQueryService"


class UserQueryService(AbstractQueryService):
    def __init__(self, view: AbstractView):
        super().__init__(view)

    @logging_decorator(LOG_PATH)
    async def get_one(self, ident: str) -> User | None:
        async with self.view:
            return await self.view.user.get(ident=ident)

    @logging_decorator(LOG_PATH)
    async def get_one_or_raise(self, ident: str) -> User:
        async with self.view:
            user = await self.view.user.get(ident=ident)
            if not user:
                raise ItemNotFound
            return user

    @logging_decorator(LOG_PATH)
    async def get_all(self, *args, **kwargs) -> list[User]:
        async with self.view:
            return await self.view.user.list(*args, **kwargs)
