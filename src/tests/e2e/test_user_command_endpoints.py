from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.common.settings import settings
from src.tests.e2e.conftest import create_test_user, create_test_user_and_login


@pytest.mark.asyncio
async def test_create_user(app_for_test: FastAPI):
    # GIVEN
    url = app_for_test.url_path_for("create_user")
    data = {
        "phone": "010",
        "email": "email@email.com",
        "password": "password",
    }

    # WHEN
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        # ASGITransport used to silence warnings by pytest
        base_url=settings.test_url,
    ) as ac:
        response = await ac.post(url, json=data)

    # THEN
    assert response.status_code == HTTPStatus.CREATED
    res = response.json()
    assert res

    # WHEN creating again
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        response = await ac.post(url, json=data)

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST


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
@pytest.mark.parametrize(
    "authorized, status",
    [
        (
            True,
            HTTPStatus.OK,
        ),
        (
            False,
            HTTPStatus.UNAUTHORIZED,
        ),
    ],
)
async def test_update_user(app_for_test: FastAPI, authorized: bool, status: HTTPStatus):
    # GIVEN
    headers, user = await create_test_user_and_login(app_for_test=app_for_test)

    # WHEN
    data = {
        "email": "email1@email.com",
        "phone": "010-1111-2222",
    }

    url = app_for_test.url_path_for("update_user", user_id=user["id"])
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        if authorized:
            res = await ac.patch(url, json=data, headers=headers)
        else:
            res = await ac.patch(url, json=data)

    # THEN
    assert res.status_code == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "authorized, status",
    [
        (
            True,
            HTTPStatus.OK,
        ),
        (
            False,
            HTTPStatus.UNAUTHORIZED,
        ),
    ],
)
async def test_delete_user(app_for_test: FastAPI, authorized: bool, status: HTTPStatus):
    # GIVEN
    headers, user = await create_test_user_and_login(app_for_test=app_for_test)

    # WHEN
    url = app_for_test.url_path_for("delete_user", user_id=user["id"])
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        if authorized:
            res = await ac.delete(url, headers=headers)
        else:
            res = await ac.delete(url)

    # THEN
    assert res.status_code == status
