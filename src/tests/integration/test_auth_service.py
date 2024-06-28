import pytest

from src.domain.user.dto import UserOut
from src.service_layer.exceptions import Forbidden, Unauthorized
from src.service_layer.service_factory import get_auth_service


@pytest.mark.asyncio
async def test_login_happy_path(create_user: UserOut, user_data: dict):
    # GIVEN
    service = get_auth_service()

    # WHEN
    token, refresh_token = await service.login(email=user_data["email"], password=user_data["password"])

    # THEN
    assert token, refresh_token


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


@pytest.mark.asyncio
async def test_refresh_token_happy_path(create_user: UserOut, user_data: dict):
    # GIVEN
    service = get_auth_service()
    _, refresh_token = await service.login(email=user_data["email"], password=user_data["password"])

    # WHEN
    token = await service.refresh(refresh_token=refresh_token, grant_type="refresh_token")

    # THEN
    assert token


@pytest.mark.asyncio
async def test_refresh_token_unhappy_path_expired_token(
    create_user: UserOut,
    user_data: dict,
    monkeypatch_jwt_settings,
):
    # GIVEN
    service = get_auth_service()
    _, refresh_token = await service.login(email=user_data["email"], password=user_data["password"])

    # WHEN
    with pytest.raises(Forbidden, match="token has expired"):  # THEN
        await service.refresh(refresh_token=refresh_token, grant_type="refresh_token")


@pytest.mark.asyncio
async def test_refresh_token_unhappy_path_invalid_token(
    create_user: UserOut,
    user_data: dict,
    monkeypatch_create_jwt_token_invalid_token,
):
    # GIVEN
    service = get_auth_service()
    _, refresh_token = await service.login(email=user_data["email"], password=user_data["password"])

    # WHEN
    with pytest.raises(Forbidden):  # THEN
        await service.refresh(refresh_token=refresh_token, grant_type="refresh_token")
