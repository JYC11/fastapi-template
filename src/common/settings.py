import os
import sys

from pydantic_settings import BaseSettings
from typing_extensions import Literal

if "pytest" in sys.modules:
    os.environ["STAGE"] = "TEST"

# if not os.getenv("STAGE"):
#     raise Exception("STAGE is not defined")


class DBSettings(BaseSettings):
    server: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "postgres"
    port: int = 5432
    pool_size: int = 10
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.db_user,
            self.db_password,
            self.server,
            self.port,
            self.db_name,
        )


class Settings(BaseSettings):
    stage: Literal["LOCAL", "TEST", "DEV", "STAGE", "PROD"] = "LOCAL"
    is_ci: bool = False
    db_settings: DBSettings = DBSettings()
    api_v1_str: str = "/api/v1"


settings = Settings()
