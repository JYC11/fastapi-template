from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.common.settings import settings


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
