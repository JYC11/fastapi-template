from typing import Any, Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.abstract_repository import AbstractRepository
from src.common.db import async_autocommit_session_factory
from src.service.abstract_view import AbstractView

DEFAULT_AUTOCOMMIT_SESSION_FACTORY = async_autocommit_session_factory


class SqlAlchemyView(AbstractView):
    def __init__(
        self,
        repositories: dict[str, Type[AbstractRepository]],
        session_factory=DEFAULT_AUTOCOMMIT_SESSION_FACTORY,
    ):
        self.repositories = repositories
        self.session_factory = session_factory
        self.user: AbstractRepository | None = None  # type: ignore
        self.failed_message_log: AbstractRepository | None = None  # type: ignore

    async def __aenter__(self) -> AbstractView:
        self.session: AsyncSession = self.session_factory()
        if self.repositories:
            for attr, repository in self.repositories.items():
                if hasattr(self, attr):
                    setattr(self, attr, repository(session=self.session))
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def _execute(self, query: Any, scalars: bool, one: bool):
        if isinstance(query, str):
            query = text(query)
        execution = await self.session.execute(query)
        if one:
            if scalars:
                return execution.scalar_one_or_none()
            return execution.one_or_none()
        else:
            if scalars:
                return execution.scalars().all()
            return execution.all()


def get_view(repositories: dict[str, Type[AbstractRepository]]) -> AbstractView:
    return SqlAlchemyView(repositories=repositories)
