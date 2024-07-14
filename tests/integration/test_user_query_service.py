import pytest
from nanoid import generate  # type: ignore

from src.domain.user.dto import UserOut, UserSearchParams
from src.entrypoints.dto import PaginationParams
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


@pytest.mark.asyncio
async def test_paginate_users_happy_path(create_users_for_pagination: list[UserOut]):
    # GIVEN
    expected = create_users_for_pagination

    # WHEN
    final_found: list[UserOut] = []
    final_total = 0
    for page, size in [(1, 10), (2, 10)]:
        service = get_user_query_service()
        found, found_total = await service.paginate(
            search_params=UserSearchParams(
                phone=None,
                email=None,
            ),
            pagination_params=PaginationParams(
                page=page,
                size=size,
                sort=None,
            ),
        )
        final_found.extend(found)
        final_total = found_total

    # THEN
    assert final_total == len(expected)
    final_found.sort(key=lambda x: x.id)
    expected.sort(key=lambda x: x.id)
    for expected, got in zip(expected, final_found):  # type: ignore
        assert expected == got
