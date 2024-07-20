from typing import Annotated

from fastapi import Depends, Security

from src.common.security.token import Token
from src.domain.user.dto import UserOut
from src.entrypoints.dto import PaginationParams
from src.entrypoints.security import get_token
from src.service_layer.message_bus import MessageBus, get_message_bus
from src.service_layer.service_factory import get_auth_service, get_user_query_service
from src.service_layer.user.authentication_service import AuthenticationService
from src.service_layer.user.query_service import UserQueryService

MessageBusDep = Annotated[MessageBus, Depends(get_message_bus)]

UserQueryServiceDep = Annotated[UserQueryService, Depends(get_user_query_service)]

AuthServiceDep = Annotated[AuthenticationService, Depends(get_auth_service)]

PaginationParamDeps = Annotated[PaginationParams, Depends(PaginationParams)]

GetToken = Annotated[Token, Security(get_token)]


async def get_current_user(
    token: GetToken,
    user_query_service: UserQueryServiceDep,
) -> UserOut:
    user: UserOut = await user_query_service.get_one_or_raise(ident=token.sub)
    return user


GetCurrentUser = Annotated[UserOut, Security(get_current_user)]
