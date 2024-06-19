from typing import Annotated

from fastapi import Depends

from src.service.message_bus import MessageBus, get_message_bus

MessageBusDep = Annotated[MessageBus, Depends(get_message_bus)]
