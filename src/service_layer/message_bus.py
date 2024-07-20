from collections import defaultdict, deque
from typing import Any, Callable, Literal, Type

from src.domain import Command, Event, Message
from src.domain.models import FailedMessageLog
from src.domain.user import commands as user_commands
from src.service_layer.abstracts.abstract_command_handler import CommandHandler
from src.service_layer.abstracts.abstract_event_handler import EventHandler
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.failed_message_log.repository import FailedMessageLogRepository
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.service_layer.user.factory import get_user_creation_handler, get_user_delete_handler, get_user_update_handler


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: dict[Type[Event], list[Callable[..., EventHandler]]],
        command_handlers: dict[Type[Command], Callable[..., CommandHandler]],
    ) -> None:
        self.queue: deque[Message] = deque()
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    async def handle(self, message: Message) -> Any | None:
        self.queue.appendleft(message)
        res: Any | None = None

        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Event):
                await self.handle_event(message)
            elif isinstance(message, Command):
                res = await self.handle_command(message)
            else:
                raise Exception(f"{message} was not a Command or Event")
        return res

    async def _add_log(self, message_type: Literal["EVENT", "COMMAND"], message_name: str, error_message: str):
        async with self.uow:
            self.uow.failed_message_log.add(
                FailedMessageLog(
                    message_type=message_type,
                    message_name=message_name,
                    error_message=error_message,
                )
            )
            await self.uow.commit()

    async def handle_event(self, event: Event):
        for handler_factory_func in self.event_handlers[type(event)]:
            try:
                service: EventHandler = handler_factory_func()
                await service.execute(event=event)
                self.queue.extendleft(service.uow.events)
            except Exception as e:
                await self._add_log(
                    message_type="EVENT",
                    message_name=type(event).__name__,
                    error_message=str(e),
                )
                raise e

    async def handle_command(self, command: Command):
        try:
            handler_factory_func = self.command_handlers[type(command)]
            service: CommandHandler = handler_factory_func()
            res = await service.execute(cmd=command)
            self.queue.extendleft(service.uow.events)
            return res
        except Exception as e:
            await self._add_log(
                message_type="COMMAND",
                message_name=type(command).__name__,
                error_message=str(e),
            )
            raise e


event_handlers: dict[Type[Event], list[Callable[..., EventHandler]]] = defaultdict(list)

command_handlers: dict[Type[Command], Callable[..., CommandHandler]] = {
    user_commands.CreateUser: get_user_creation_handler,
    user_commands.UpdateUser: get_user_update_handler,
    user_commands.DeleteUser: get_user_delete_handler,
}


def get_message_bus():
    return MessageBus(
        uow=SqlAlchemyUnitOfWork(repositories=dict(failed_message_log=FailedMessageLogRepository)),
        event_handlers=event_handlers,
        command_handlers=command_handlers,
    )
