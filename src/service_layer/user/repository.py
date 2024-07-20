from sqlalchemy.ext.asyncio.session import AsyncSession

from src.adapters.sqlalchemy_repository import SqlAlchemyRepository
from src.domain.user.model import User


class UserRepository(SqlAlchemyRepository[User]):  # type: ignore
    def __init__(self, session: AsyncSession):
        super(UserRepository, self).__init__(session, User)
