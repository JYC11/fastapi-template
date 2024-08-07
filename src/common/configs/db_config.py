from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.persistent_orm import start_mappers
from src.common.configs.settings import settings

engine: AsyncEngine | None = None
autocommit_engine: AsyncEngine | None = None
async_transactional_session_factory: sessionmaker | None = None
async_autocommit_session_factory: sessionmaker | None = None


if settings.stage != "TEST" or settings.is_ci is True:
    engine = create_async_engine(
        settings.db_settings.url,
        pool_pre_ping=True,
        pool_size=settings.db_settings.pool_size,
        max_overflow=settings.db_settings.max_overflow,
        future=True,
    )
    async_transactional_session_factory = sessionmaker(
        engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
    )
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    async_autocommit_session_factory = sessionmaker(autocommit_engine, expire_on_commit=False, class_=AsyncSession)
    start_mappers()
