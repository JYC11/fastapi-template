from datetime import datetime
from typing import Any
from uuid import uuid4

from jose import ExpiredSignatureError, jwt
from pydantic import BaseModel

from src.common.settings import settings


class TokenExpired(Exception): ...


class InvalidToken(Exception): ...


class Token(BaseModel):
    email: str
    phone: str
    exp: str
    sub: str
    iat: str
    jti: str


def create_jwt_token(
    subject: str,
    private_claims: dict[str, Any] | None,
    refresh: bool,
):
    expiration_delta = (
        settings.jwt_settings.refresh_expiration_delta if refresh else settings.jwt_settings.expiration_delta
    )
    expiration_datetime = datetime.now() + expiration_delta
    registered_claims = {"exp": expiration_datetime, "sub": subject, "iat": datetime.utcnow(), "jti": uuid4().hex}
    claims = registered_claims | private_claims if private_claims else registered_claims
    jwt_token = jwt.encode(
        claims=claims,
        key=settings.jwt_settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_settings.algorithm,
    )
    return jwt_token


def validate_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token=token, key=settings.jwt_settings.secret_key.get_secret_value())
        return Token(**decoded_token)
    except ExpiredSignatureError:
        raise TokenExpired("token has expired")
    except Exception as e:
        raise InvalidToken(f"token is invalid: {str(e)}")
