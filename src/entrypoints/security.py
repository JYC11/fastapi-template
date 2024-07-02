from typing import Annotated

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from src.common.security.token import Token, validate_jwt_token
from src.common.settings import settings
from src.domain.user.dto import UserOut
from src.entrypoints.depdencies import UserQueryServiceDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api_v1_login_url)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_query_service: UserQueryServiceDep):
    decoded_token: Token = validate_jwt_token(token=token)
    user: UserOut = await user_query_service.get_one_or_raise(ident=decoded_token.sub)
    return user
