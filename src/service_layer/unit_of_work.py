from collections import deque
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from src.adapters.abstract_repository import AbstractRepository
from src.common.db import async_transactional_session_factory
from src.domain import Message
from src.service_layer import exceptions
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork

DEFAULT_TRANSACTIONAL_SESSION_FACTORY = async_transactional_session_factory


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        repositories: dict[str, Type[AbstractRepository]],
        session_factory=DEFAULT_TRANSACTIONAL_SESSION_FACTORY,
    ):
        self.repositories = repositories
        self.events: deque[Message] = deque()
        self.session_factory = session_factory
        self.user: AbstractRepository | None = None  # type: ignore
        self.failed_message_log: AbstractRepository | None = None  # type: ignore

    async def __aenter__(self) -> AbstractUnitOfWork:
        self.session: AsyncSession = self.session_factory()
        if self.repositories:
            for attr, repository in self.repositories.items():
                if hasattr(self, attr):
                    setattr(self, attr, repository(session=self.session))
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await self.session.close()

    async def _commit(self):
        try:
            await self.session.commit()
        except StaleDataError:
            await self.session.rollback()
            raise exceptions.ConcurrencyException

    async def _flush(self):
        await self.session.flush()

    async def _rollback(self):
        await self.session.rollback()

    async def _refresh(self, object):
        await self.session.refresh(object)


def get_uow(repositories: dict[str, Type[AbstractRepository]]) -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(repositories=repositories)
