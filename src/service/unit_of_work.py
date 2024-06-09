from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from src.adapters.abstract_repository import AbstractRepository
from src.common.db import async_transactional_session_factory
from src.service import exceptions
from src.service.abstract_unit_of_work import AbstractUnitOfWork

DEFAULT_TRANSACTIONAL_FACTORY = async_transactional_session_factory
assert DEFAULT_TRANSACTIONAL_FACTORY is not None


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        repositories: dict[str, Type[AbstractRepository]],
        session_factory=DEFAULT_TRANSACTIONAL_FACTORY,
    ):
        self.repositories = repositories
        self.session_factory = session_factory

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

    async def _rollback(self):
        await self.session.rollback()

    async def _refresh(self, object):
        await self.session.refresh(object)
