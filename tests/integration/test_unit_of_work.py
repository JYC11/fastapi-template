import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models import User
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.user.repository import UserRepository


@pytest.mark.asyncio
async def test_can_get_record_and_update_it(uow: AbstractUnitOfWork, session: AsyncSession):
    # GIVEN
    uow.repositories = dict(user=UserRepository)
    async with uow:
        email = "test@email.com"
        uow.user.add(User(email=email, phone="1234", password="password"))
        await uow.flush()
        found_user: User | None = await uow.user.get_by(email__eq=email)
        assert found_user is not None
        assert found_user.email == email

        # WHEN
        new_phone = "5678"
        found_user.phone = new_phone
        await uow.commit()

    # THEN
    execution = await session.execute(select(User).where(User.email == email))
    user: User | None = execution.scalar_one_or_none()
    assert user.phone == new_phone


@pytest.mark.asyncio
async def test_will_rollback_uncommitted(uow: AbstractUnitOfWork):
    # GIVEN
    uow.repositories = dict(user=UserRepository)

    uow.repositories = dict(user=UserRepository)
    async with uow:
        # WHEN
        uow.user.add(User(email="test@email.com", phone="1234", password="password"))

    # THEN
    async with uow:
        users: list[User] = await uow.user.get_all()
        assert len(users) == 0


@pytest.mark.asyncio
async def test_will_rollback_on_error(uow: AbstractUnitOfWork):
    # GIVEN
    uow.repositories = dict(user=UserRepository)

    class ContrivedException(Exception): ...

    uow.repositories = dict(user=UserRepository)
    with pytest.raises(ContrivedException):
        async with uow:
            # WHEN
            uow.user.add(User(email="test@email.com", phone="1234", password="password"))
            raise ContrivedException

    # THEN
    async with uow:
        users: list[User] = await uow.user.get_all()
        assert len(users) == 0
