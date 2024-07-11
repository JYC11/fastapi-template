from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.common.configs.settings import settings
from src.tests.e2e.conftest import create_test_user, create_test_user_and_login


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, status",
    [
        (
            {
                "username": "email@email.com",
                "password": "password",
            },
            HTTPStatus.OK,
        ),
        (
            {
                "username": "email@email.com",
                "password": "password1",
            },
            HTTPStatus.UNAUTHORIZED,
        ),
    ],
)
async def test_login_user(app_for_test: FastAPI, data: dict, status: HTTPStatus):
    # GIVEN
    await create_test_user(app_for_test=app_for_test)

    url = app_for_test.url_path_for("login_user")
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        res = await ac.post(url, data=data)

    # THEN
    assert res.status_code == status
    if status == HTTPStatus.OK:
        data = res.json()
        assert data["token"], data["refresh_token"]


@pytest.mark.asyncio
async def test_refresh_token(app_for_test: FastAPI):
    # GIVEN
    headers, user = await create_test_user_and_login(app_for_test=app_for_test)

    # WHEN
    data = {
        "grant_type": "refresh_token",
        "refresh_token": headers["Authorization"].replace("Bearer ", ""),
    }

    url = app_for_test.url_path_for("refresh_token")
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        res = await ac.post(url, json=data)

    # THEN
    data = res.json()
    assert res.status_code == HTTPStatus.OK
