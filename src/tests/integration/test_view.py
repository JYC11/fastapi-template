import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models import User
from src.service.abstracts.abstract_view import AbstractView
from src.service.user.repository import UserRepository


@pytest.mark.asyncio
async def test_can_get_from_view_with_repository(session: AsyncSession, view_: AbstractView):
    # GIVEN
    user = User(email="test@email.com", phone="1234", password="password")
    session.add(user)
    await session.commit()

    view_.repositories = dict(user=UserRepository)

    # WHEN
    async with view_:
        found: User | None = await view_.user.get(ident=user.id)

        # THEN
        assert user == found


@pytest.mark.asyncio
async def test_can_get_from_view_with_raw_query(session: AsyncSession, view_: AbstractView):
    # GIVEN
    user = User(email="test@email.com", phone="1234", password="password")
    session.add(user)
    await session.commit()

    view_.repositories = dict(user=UserRepository)

    # WHEN
    async with view_:
        query = f"""
        SELECT * FROM user WHERE id = '{user.id}';
        """

        res = await view_.execute(query=query, scalars=False, one=True)
        assert res is not None
        assert res.email == user.email
        assert res.phone == user.phone
        assert res.password == user.password


@pytest.mark.asyncio
async def test_can_get_from_view_with_sqlalchemy_query(session: AsyncSession, view_: AbstractView):
    # GIVEN
    user = User(email="test@email.com", phone="1234", password="password")
    session.add(user)
    await session.commit()

    view_.repositories = dict(user=UserRepository)

    # WHEN
    async with view_:
        query = select(User).where(User.id == user.id)

        res = await view_.execute(query=query, scalars=True, one=True)
        assert res is not None
        assert res.email == user.email
        assert res.phone == user.phone
        assert res.password == user.password
