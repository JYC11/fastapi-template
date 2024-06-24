import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.commands import CreateUser
from src.domain.user.dto import UserOut
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.service_factory import get_user_command_service, get_user_query_service


@pytest.mark.asyncio
async def test_delete_user(uow: AbstractUnitOfWork, session: AsyncSession):
    # GIVEN
    command_service = get_user_command_service()
    created = await command_service.create(cmd=CreateUser(email="test@email.com", phone="1234", password="password"))
    assert isinstance(created, UserOut)

    # WHEN
    service = get_user_query_service()
    found = await service.get_one(ident=created.id)

    # THEN
    assert isinstance(found, UserOut)
    assert found == created
