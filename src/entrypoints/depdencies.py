from typing import Annotated

from fastapi import Depends

from src.entrypoints.dto import PaginationParams
from src.service_layer.message_bus import MessageBus, get_message_bus
from src.service_layer.service_factory import get_user_query_service
from src.service_layer.user.query_service import UserQueryService

MessageBusDep = Annotated[MessageBus, Depends(get_message_bus)]

UserQueryServiceDep = Annotated[UserQueryService, Depends(get_user_query_service)]

PaginationParamDeps = Annotated[PaginationParams, Depends(PaginationParams)]
