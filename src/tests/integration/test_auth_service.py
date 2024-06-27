import pytest

from src.domain.user.dto import UserOut
from src.service_layer.exceptions import Unauthorized
from src.service_layer.service_factory import get_auth_service


@pytest.mark.asyncio
async def test_login_happy_path(create_user: UserOut, user_data: dict):
    # GIVEN
    service = get_auth_service()

    # WHEN
    tokens = await service.login(email=user_data["email"], password=user_data["password"])

    # THEN
    assert tokens


@pytest.mark.asyncio
async def test_login_unhappy_path(create_user: UserOut, user_data: dict):
    # GIVEN
    service = get_auth_service()

    # WHEN
    with pytest.raises(Unauthorized):  # THEN
        await service.login(email="email", password=user_data["password"])

    # WHEN
    with pytest.raises(Unauthorized):  # THEN
        await service.login(email=user_data["email"], password="incorrect password")
