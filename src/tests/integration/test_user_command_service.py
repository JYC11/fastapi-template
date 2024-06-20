import pytest
from argon2 import PasswordHasher
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User
from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.events import UserCreated, UserDeleted, UserUpdated
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.service_factory import get_user_command_service


@pytest.mark.asyncio
async def test_create_user(uow: AbstractUnitOfWork):
    # GIVEN
    service = get_user_command_service()
    hasher = PasswordHasher()
    email = "test@email.com"
    phone = "1234"
    password = "password"

    # WHEN
    user = await service.create(cmd=CreateUser(email=email, phone=phone, password=password))
    assert isinstance(user, User)

    # THEN
    assert user.email == email
    assert user.phone == phone
    assert hasher.verify(user.password, password)
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserCreated)
    assert service.uow.events[0].id == user.id


@pytest.mark.asyncio
async def test_update_user(uow: AbstractUnitOfWork):
    # GIVEN
    service = get_user_command_service()
    hasher = PasswordHasher()
    email = "test@email.com"
    phone = "1234"
    password = "password"
    new_email = "test1@email.com"
    new_phone = "5678"

    created = await service.create(cmd=CreateUser(email=email, phone=phone, password=password))

    # WHEN
    user = await service.update(cmd=UpdateUser(id=created.id, email=new_email, phone=new_phone))
    assert isinstance(user, User)

    # THEN
    assert user.email != email
    assert user.phone != phone
    assert user.email == new_email
    assert user.phone == new_phone
    assert hasher.verify(user.password, password)
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserUpdated)
    assert service.uow.events[0].id == user.id


@pytest.mark.asyncio
async def test_delete_user(uow: AbstractUnitOfWork, session: AsyncSession):
    # GIVEN
    service = get_user_command_service()
    user = await service.create(cmd=CreateUser(email="test@email.com", phone="1234", password="password"))
    assert isinstance(user, User)

    # WHEN
    await service.delete(cmd=DeleteUser(id=user.id))

    # THEN
    execution = await session.execute(text(f"SELECT * FROM user WHERE id = '{user.id}'"))
    found = execution.one_or_none()
    assert found is None
    assert len(service.uow.events) == 1
    assert isinstance(service.uow.events[0], UserDeleted)
    assert service.uow.events[0].id == user.id
