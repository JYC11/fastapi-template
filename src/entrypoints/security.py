from typing import Annotated

from fastapi import HTTPException, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer
from starlette import status

from src.common.configs.settings import settings
from src.common.security.token import InvalidToken, Token, TokenExpired, validate_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api_v1_login_url)


def get_token(
    token: Annotated[str, Security(oauth2_scheme)],
) -> Token:
    try:
        decoded_token: Token = validate_jwt_token(token)
        return decoded_token
    except TokenExpired as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InvalidToken as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
