import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models import User


@pytest.mark.asyncio
async def test_can_connect(session: AsyncSession):
    session.add(User(phone="111", email="email", password="password"))
    await session.commit()
    query = await session.execute(select(User))
    _user: User | None = query.scalars().first()
    assert True
