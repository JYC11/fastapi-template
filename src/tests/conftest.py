import asyncio
from base64 import b64encode
from datetime import timedelta
from typing import AsyncGenerator, Generator, Type

import pytest
import pytest_asyncio
from decouple import config  # type: ignore
from fastapi.applications import FastAPI
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from starlette.testclient import TestClient

from src.adapters.abstract_repository import AbstractRepository
from src.adapters.in_memory_orm import metadata, start_mappers
from src.common import security
from src.common.settings import settings
from src.main import app
from src.service_layer import unit_of_work, view
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.abstracts.abstract_view import AbstractView
from src.service_layer.failed_message_log.repository import FailedMessageLogRepository
from src.service_layer.message_bus import MessageBus, command_handlers, event_handlers, get_message_bus
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.service_layer.view import SqlAlchemyView

# DB STUFF FROM HERE
# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    async with engine.connect() as conn:
        async with conn.begin():
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
    start_mappers()
    yield engine
    clear_mappers()


@pytest_asyncio.fixture(scope="function")
async def session_factory(async_engine: AsyncEngine) -> AsyncGenerator[async_scoped_session, None]:
    async with async_engine.connect() as conn:
        session_factory: async_scoped_session = async_scoped_session(
            sessionmaker(
                conn,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=asyncio.current_task,
        )
        try:
            yield session_factory
        finally:
            async with async_engine.connect() as _conn:
                async with _conn.begin():
                    for table in reversed(metadata.sorted_tables):
                        await _conn.execute(table.delete())
                    await _conn.commit()


@pytest_asyncio.fixture(scope="function")
async def session(session_factory):
    async with session_factory() as _session:
        yield _session


# DEPENDENCIES AND FAKE DEPENDENCIES
@pytest_asyncio.fixture(scope="function")
def uow(session_factory) -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(
        session_factory=session_factory,
        repositories=dict(),
    )


@pytest_asyncio.fixture(scope="function")
def view_(session_factory) -> AbstractView:
    return SqlAlchemyView(
        session_factory=session_factory,
        repositories=dict(),
    )


@pytest_asyncio.fixture(scope="function", autouse=True)
def monkeypatch_get_unit_of_work(monkeypatch, session_factory):
    def get_test_uow(repositories: dict[str, Type[AbstractRepository]]) -> AbstractUnitOfWork:
        return SqlAlchemyUnitOfWork(
            repositories=repositories,
            session_factory=session_factory,
        )

    monkeypatch.setattr(unit_of_work, "get_uow", get_test_uow)


@pytest_asyncio.fixture(scope="function", autouse=True)
def monkeypatch_get_view(monkeypatch, session_factory):
    def get_test_view(repositories: dict[str, Type[AbstractRepository]]) -> AbstractView:
        return SqlAlchemyView(
            repositories=repositories,
            session_factory=session_factory,
        )

    monkeypatch.setattr(view, "get_view", get_test_view)


@pytest_asyncio.fixture(scope="function")
def message_bus(uow: AbstractUnitOfWork) -> MessageBus:
    uow.repositories = dict(failed_message_log=FailedMessageLogRepository)
    return MessageBus(
        uow=uow,
        event_handlers=event_handlers,
        command_handlers=command_handlers,
    )


@pytest.fixture(scope="function")
def client(message_bus: MessageBus):

    # dependency injection here
    app.dependency_overrides[get_message_bus] = lambda: message_bus

    with TestClient(app) as c:
        yield c


@pytest.fixture
def app_for_test(message_bus: MessageBus) -> Generator[FastAPI, None, None]:
    # dependency overrides here
    app.dependency_overrides[get_message_bus] = lambda: message_bus

    yield app


# DATA
@pytest_asyncio.fixture
def user_data():
    return {"email": "test@email.com", "phone": "01011112222", "password": "secret"}


@pytest_asyncio.fixture
def monkeypatch_jwt_settings(monkeypatch):
    class FakeJwtSettings(BaseSettings):
        raw_secret_key: SecretStr = SecretStr(config("RAW_SECRET_KEY"))
        public_key: str | None = None
        private_key: str | None = None
        algorithm: str = "HS256"
        authorization_type: str = "Bearer"
        verify: bool = True
        verify_expiration: bool = True
        expiration_delta: timedelta = timedelta(seconds=-1)
        refresh_expiration_delta: timedelta = timedelta(seconds=-1)
        allow_refresh: bool = True
        access_toke_expire_minutes: int = 60 * 24 * 8

        @property
        def secret_key(self):
            return SecretStr(b64encode(self.raw_secret_key.get_secret_value().encode()).decode())

    fake_jwt_settings = FakeJwtSettings()

    monkeypatch.setattr(settings, "jwt_settings", fake_jwt_settings)


@pytest_asyncio.fixture
def monkeypatch_create_jwt_token_invalid_token(monkeypatch):
    def create_invalid_token(*args, **kwargs):
        return "token"

    monkeypatch.setattr(security, "create_jwt_token", create_invalid_token)
