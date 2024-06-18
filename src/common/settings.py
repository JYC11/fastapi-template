import os
import sys

from pydantic_settings import BaseSettings
from typing_extensions import Literal

if "pytest" in sys.modules:
    os.environ["STAGE"] = "TEST"

if not os.getenv("STAGE"):
    raise Exception("STAGE is not defined")


class DBSettings(BaseSettings):
    server: str = "localhost"
    user: str = "admin"
    password: str = "root"
    db: str = "postgres"
    port: int = 5432
    pool_size: int = 10
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.server,
            self.port,
            self.db,
        )


class Settings(BaseSettings):
    stage: Literal["LOCAL", "TEST", "DEV", "STAGE", "PROD"] = "LOCAL"
    is_ci: bool = False
    db_settings: DBSettings = DBSettings()


settings = Settings()
