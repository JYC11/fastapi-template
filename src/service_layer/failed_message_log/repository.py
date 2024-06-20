from sqlalchemy.ext.asyncio.session import AsyncSession

from src.adapters.sqlalchemy_repository import SqlAlchemyRepository
from src.domain.models import FailedMessageLog


class FailedMessageLogRepository(SqlAlchemyRepository[FailedMessageLog]):  # type: ignore
    def __init__(self, session: AsyncSession):
        super(FailedMessageLogRepository, self).__init__(session, FailedMessageLog)
