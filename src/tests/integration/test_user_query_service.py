import pytest
from nanoid import generate  # type: ignore

from src.domain.user.dto import UserOut
from src.service_layer.exceptions import ItemNotFound
from src.service_layer.service_factory import get_user_query_service


@pytest.mark.asyncio
async def test_get_one_user_happy_path(create_user: UserOut):
    # GIVEN
    created = create_user

    # WHEN
    service = get_user_query_service()
    found = await service.get_one_or_raise(ident=created.id)

    # THEN
    assert isinstance(found, UserOut)
    assert found == created


@pytest.mark.asyncio
async def test_get_one_user_unhappy_path():
    # GIVEN
    service = get_user_query_service()

    # WHEN
    with pytest.raises(ItemNotFound):
        await service.get_one_or_raise(ident=generate())
