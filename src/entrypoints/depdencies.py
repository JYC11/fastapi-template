from typing import Annotated

from fastapi import Depends

from src.service.factory import get_user_query_service
from src.service.message_bus import MessageBus, get_message_bus
from src.service.user.query_service import UserQueryService

MessageBusDep = Annotated[MessageBus, Depends(get_message_bus)]

UserQueryServiceDep = Annotated[UserQueryService, Depends(get_user_query_service)]
