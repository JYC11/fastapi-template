import sys
from base64 import b64encode
from datetime import timedelta
from typing import Literal

from decouple import config  # type: ignore
from pydantic import SecretStr
from pydantic_settings import BaseSettings

if not config("STAGE"):
    raise Exception("STAGE is not defined")


class DBSettings(BaseSettings):
    db_server: str = config("DB_SERVER")
    db_user: str = config("DB_USER")
    db_password: SecretStr = SecretStr(config("DB_PASSWORD"))
    db_name: str = config("DB_NAME")
    db_port: int = config("DB_PORT")
    pool_size: int = 10
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.db_user,
            self.db_password.get_secret_value(),
            self.db_server,
            self.db_port,
            self.db_name,
        )


class JWTSettings(BaseSettings):
    raw_secret_key: SecretStr = SecretStr(config("RAW_SECRET_KEY"))
    public_key: str | None = None
    private_key: str | None = None
    algorithm: str = "HS256"
    authorization_type: str = "Bearer"
    verify: bool = True
    verify_expiration: bool = True
    expiration_delta: timedelta = timedelta(minutes=30)
    refresh_expiration_delta: timedelta = timedelta(days=15)
    allow_refresh: bool = True
    access_toke_expire_minutes: int = 60 * 24 * 8

    @property
    def secret_key(self):
        return SecretStr(b64encode(self.raw_secret_key.get_secret_value().encode()).decode())


class Settings(BaseSettings):
    stage: Literal["LOCAL", "TEST", "DEV", "STAGE", "PROD"] = config("STAGE")
    is_ci: bool = False
    db_settings: DBSettings = DBSettings()
    jwt_settings: JWTSettings = JWTSettings()
    api_v1_str: str = "/api/v1"


settings = Settings()

if "pytest" in sys.modules:
    settings.stage = "TEST"
