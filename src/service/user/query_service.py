from src.domain.models import User
from src.service.abstracts.abstract_query_service import AbstractQueryService
from src.service.abstracts.abstract_view import AbstractView
from src.service.exceptions import ItemNotFound


class UserQueryService(AbstractQueryService):
    def __init__(self, view: AbstractView):
        super().__init__(view)

    async def get_one(self, ident: str) -> User | None:
        async with self.view:
            return await self.view.user.get(ident=ident)

    async def get_one_or_raise(self, ident: str) -> User:
        async with self.view:
            user = await self.view.user.get(ident=ident)
            if not user:
                raise ItemNotFound
            return user

    async def get_all(self, *args, **kwargs) -> list[User]:
        async with self.view:
            return await self.view.user.list(*args, **kwargs)
