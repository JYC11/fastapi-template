from collections import defaultdict, deque

from typing_extensions import Any, Callable, Type

from src.domain import Message
from src.domain.command import Command
from src.domain.event import Event
from src.domain.models import FailedMessageLog
from src.service.abstract_service import AbstractService
from src.service.abstract_unit_of_work import AbstractUnitOfWork
from src.service.factory import get_user_service
from src.service.failed_message_log.repository import FailedMessageLogRepository
from src.service.unit_of_work import SqlAlchemyUnitOfWork
from src.service.user import commands as user_commands


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: dict[Type[Event], list[tuple[Callable[..., AbstractService], str]]],
        command_handlers: dict[Type[Command], tuple[Callable[..., AbstractService], str]],
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

    async def handle_event(self, event: Event):
        for service_factory_func, method_name in self.event_handlers[type(event)]:
            try:
                service: AbstractService = service_factory_func()
                await service.handle_event(method_name=method_name, event=event)
                self.queue.extendleft(service.uow.events)
            except Exception as e:
                async with self.uow:
                    self.uow.failed_message_log.add(
                        FailedMessageLog(message_type="EVENT", message_name=type(event).__name__, error_message=str(e))
                    )
                    await self.uow.commit()

    async def handle_command(self, command: Command):
        try:
            service_factory_func, method_name = self.command_handlers[type(command)]
            service: AbstractService = service_factory_func()
            res = await service.handle_command(method_name=method_name, command=command)
            self.queue.extendleft(service.uow.events)
            return res
        except Exception as e:
            async with self.uow:
                self.uow.failed_message_log.add(
                    FailedMessageLog(message_type="COMMAND", message_name=type(command).__name__, error_message=str(e))
                )
                await self.uow.commit()


def get_message_bus():
    return MessageBus(
        uow=SqlAlchemyUnitOfWork(repositories=dict(failed_message_log=FailedMessageLogRepository)),
        event_handlers=defaultdict(list),
        command_handlers={
            user_commands.CreateUser: (get_user_service, "create"),
            user_commands.UpdateUser: (get_user_service, "update"),
            user_commands.DeleteUser: (get_user_service, "delete"),
        },
    )
