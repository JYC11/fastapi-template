import pytest
from nanoid import generate  # type: ignore
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.dto import UserOut
from src.domain.user.events import UserCreated, UserDeleted, UserUpdated
from src.service_layer.abstracts.abstract_command_handler import CommandHandler
from src.service_layer.exceptions import DuplicateRecord, ItemNotFound
from src.service_layer.user.factory import get_user_creation_handler, get_user_delete_handler, get_user_update_handler


@pytest.mark.asyncio
async def test_create_user_happy_path():
    # GIVEN
    service: CommandHandler = get_user_creation_handler()
    email = "test@email.com"
    phone = "1234"
    password = "password"

    # WHEN
    user = await service.execute(cmd=CreateUser(email=email, phone=phone, password=password))
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
    service: CommandHandler = get_user_creation_handler()

    created = create_user

    # WHEN
    with pytest.raises(DuplicateRecord):  # THEN
        await service.execute(
            cmd=CreateUser(
                email=created.email,
                phone="phone",
                password="password",
            )
        )

    # WHEN
    with pytest.raises(DuplicateRecord):  # THEN
        await service.execute(
            cmd=CreateUser(
                email="email",
                phone=created.phone,
                password="password",
            )
        )


@pytest.mark.asyncio
async def test_update_user_happy_path(create_user: UserOut):
    # GIVEN
    service: CommandHandler = get_user_update_handler()
    new_email = "test1@email.com"
    new_phone = "5678"

    created = create_user

    # WHEN
    user = await service.execute(
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
    service: CommandHandler = get_user_update_handler()

    # WHEN
    with pytest.raises(ItemNotFound):  # THEN
        await service.execute(
            cmd=UpdateUser(
                id=generate(),
                email="test1@email.com",
                phone="5678",
            )
        )


@pytest.mark.asyncio
async def test_delete_user_happy_path(create_user: UserOut, session: AsyncSession):
    # GIVEN
    service: CommandHandler = get_user_delete_handler()
    created = create_user

    # WHEN
    await service.execute(cmd=DeleteUser(id=created.id))

    # THEN
    execution = await session.execute(text(f"SELECT * FROM user WHERE id = '{created.id}'"))
    found = execution.one_or_none()
    assert found is None
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserDeleted)
    assert service.uow.events[0].id == created.id
