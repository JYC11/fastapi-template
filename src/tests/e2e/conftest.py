from http import HTTPStatus

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.common.settings import settings


async def create_test_user(app_for_test: FastAPI) -> dict:
    user_data_in = {
        "phone": "010",
        "email": "email@email.com",
        "password": "password",
    }
    create_url = app_for_test.url_path_for("create_user")
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        res = await ac.post(create_url, json=user_data_in)
    assert res.status_code == HTTPStatus.CREATED
    return res.json()


async def test_user_login(app_for_test: FastAPI) -> dict:
    login_data = {
        "username": "email@email.com",
        "password": "password",
    }

    login_url = app_for_test.url_path_for("login_user")
    async with AsyncClient(
        transport=ASGITransport(app=app_for_test),  # type: ignore
        base_url=settings.test_url,
    ) as ac:
        logged_in_res = await ac.post(login_url, data=login_data)
    assert logged_in_res.status_code == HTTPStatus.OK
    return logged_in_res.json()


# if I want to just test with authenticated user
async def create_test_user_and_login(app_for_test: FastAPI):
    user_id = await create_test_user(app_for_test=app_for_test)
    res = await test_user_login(app_for_test=app_for_test)
    return ({"Authorization": f"Bearer {res['token']}"}, user_id)
