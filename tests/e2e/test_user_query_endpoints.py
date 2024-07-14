from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.common.configs.settings import settings
from tests.e2e.conftest import create_test_user_and_login, create_users_for_pagination


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
async def test_get_user(app_for_test: FastAPI, authorized: bool, status: HTTPStatus):
    # GIVEN
    headers, user = await create_test_user_and_login(app_for_test=app_for_test)

    # WHEN
    url = app_for_test.url_path_for("get_one_user", user_id=user["id"])
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        if authorized:
            res = await ac.get(url, headers=headers)
        else:
            res = await ac.get(url)

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
async def test_paginate_users(app_for_test: FastAPI, authorized: bool, status: HTTPStatus):
    # GIVEN
    headers, _ = await create_test_user_and_login(app_for_test=app_for_test)
    await create_users_for_pagination(app_for_test=app_for_test)

    # WHEN
    url = app_for_test.url_path_for("paginate_users")
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        if authorized:
            res = await ac.get(url, headers=headers)
        else:
            res = await ac.get(url)

    # THEN
    assert res.status_code == status
