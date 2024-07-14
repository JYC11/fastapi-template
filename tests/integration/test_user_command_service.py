import pytest
from nanoid import generate  # type: ignore
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.dto import UserOut
from src.domain.user.events import UserCreated, UserDeleted, UserUpdated
from src.service_layer.abstracts.abstract_service import AbstractService
from src.service_layer.exceptions import DuplicateRecord, ItemNotFound
from src.service_layer.service_factory import get_user_command_service


@pytest.mark.asyncio
async def test_create_user_happy_path():
    # GIVEN
    service = get_user_command_service()
    email = "test@email.com"
    phone = "1234"
    password = "password"

    # WHEN
    user = await service.create(cmd=CreateUser(email=email, phone=phone, password=password))
    assert isinstance(user, UserOut)

    # THEN
    assert user.email == email
    assert user.phone == phone
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserCreated)
    assert service.uow.events[0].id == user.id


@pytest.mark.asyncio
async def test_create_user_unhappy_path(create_user: UserOut):
    # GIVEN
    service: AbstractService = get_user_command_service()

    created = create_user

    # WHEN
    with pytest.raises(DuplicateRecord):  # THEN
        await service.create(
            cmd=CreateUser(
                email=created.email,
                phone="phone",
                password="password",
            )
        )

    # WHEN
    with pytest.raises(DuplicateRecord):  # THEN
        await service.create(
            cmd=CreateUser(
                email="email",
                phone=created.phone,
                password="password",
            )
        )


@pytest.mark.asyncio
async def test_update_user_happy_path(create_user: UserOut):
    # GIVEN
    service: AbstractService = get_user_command_service()
    new_email = "test1@email.com"
    new_phone = "5678"

    created = create_user

    # WHEN
    user = await service.update(
        cmd=UpdateUser(
            id=created.id,
            email=new_email,
            phone=new_phone,
        )
    )
    assert isinstance(user, UserOut)

    # THEN
    assert user.email != created.email
    assert user.phone != created.phone
    assert user.email == new_email
    assert user.phone == new_phone
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserUpdated)
    assert service.uow.events[0].id == user.id


@pytest.mark.asyncio
async def test_update_user_unhappy_path():
    # GIVEN
    service: AbstractService = get_user_command_service()

    # WHEN
    with pytest.raises(ItemNotFound):  # THEN
        await service.update(
            cmd=UpdateUser(
                id=generate(),
                email="test1@email.com",
                phone="5678",
            )
        )


@pytest.mark.asyncio
async def test_delete_user_happy_path(create_user: UserOut, session: AsyncSession):
    # GIVEN
    service = get_user_command_service()
    created = create_user

    # WHEN
    await service.delete(cmd=DeleteUser(id=created.id))

    # THEN
    execution = await session.execute(text(f"SELECT * FROM user WHERE id = '{created.id}'"))
    found = execution.one_or_none()
    assert found is None
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserDeleted)
    assert service.uow.events[0].id == created.id


@pytest.mark.asyncio
async def test_delete_user_unhappy_path():
    # GIVEN
    service: AbstractService = get_user_command_service()

    # WHEN
    with pytest.raises(ItemNotFound):  # THEN
        await service.update(
            cmd=DeleteUser(
                id=generate(),
            )
        )
