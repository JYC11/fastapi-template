import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User
from src.service_layer.user.repository import UserRepository


@pytest.mark.asyncio
async def test_repository(session: AsyncSession):
    # GIVEN
    repository = UserRepository(session=session)
    email = "test1@email.com"
    phone = "1234"
    user = User(email=email, password="password", phone=phone)
    repository.add(user)
    await session.commit()

    # WHEN
    found_by_pk: User | None = await repository.get(ident=user.id)
    assert found_by_pk is not None

    # THEN
    assert found_by_pk.create_date is not None
    assert found_by_pk.update_date is None
    assert found_by_pk.email == user.email
    assert found_by_pk.password == user.password
    assert found_by_pk.phone == user.phone

    # WHEN find by pk
    found_by_email: User | None = await repository.get_by(email__eq=email)
    assert found_by_email is not None

    # THEN find by email
    assert found_by_email.email == user.email
    assert found_by_email.password == user.password
    assert found_by_email.phone == user.phone

    # WHEN find by phone
    found_by_phone: User | None = await repository.get_by(phone__eq=phone)
    assert found_by_phone is not None

    # THEN
    assert found_by_phone.email == user.email
    assert found_by_phone.password == user.password
    assert found_by_phone.phone == user.phone

    # WHEN find all
    repository.add_all(
        [
            User(email="test2@email.com", password="password", phone="5678"),
            User(email="test3@email.com", password="password", phone="9101112"),
        ]
    )
    await session.commit()
    users: list[User] = await repository.list()
    assert len(users) > 0

    # THEN
    assert len(users) == 3

    # WHEN delete
    await repository.remove(ident=user.id)

    # THEN
    after_delete_users: list[User] = await repository.list()
    assert len(after_delete_users) == 2
