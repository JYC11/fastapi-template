from typing import Callable, Type

import pytest
from sqlalchemy.ext.asyncio import async_scoped_session

from src.domain import Command, Event
from src.domain.base import FailedMessageLog
from src.service_layer.abstracts.abstract_command_handler import CommandHandler
from src.service_layer.abstracts.abstract_event_handler import EventHandler
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.message_bus import MessageBus
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork


class CreateSomething(Command): ...


class RaiseException(Command): ...


class SomethingCreated(Event):
    message: str


class ExampleException(Exception): ...


class fake_async_scoped_session(async_scoped_session):
    def __init__(self): ...


class SomethingCreationHandler(CommandHandler):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, cmd: CreateSomething) -> str:
        self.uow.events.append(SomethingCreated(message="wow"))
        return "something"


class RaiseExceptionHandler(CommandHandler):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, cmd: RaiseException):
        raise ExampleException()


class SomethingCreatedHandler(EventHandler):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, event: SomethingCreated) -> None:
        print(f"{event.message}, something was created")


def get_fake_uow():
    return SqlAlchemyUnitOfWork(
        session_factory=fake_async_scoped_session,
        repositories=dict(),
    )


def get_something_creation_handler() -> CommandHandler:
    return SomethingCreationHandler(uow=get_fake_uow())


def get_raise_exception_handler() -> CommandHandler:
    return RaiseExceptionHandler(uow=get_fake_uow())


def get_something_created_handler() -> EventHandler:
    return SomethingCreatedHandler(uow=get_fake_uow())


event_handlers: dict[Type[Event], list[Callable[..., EventHandler]]] = {
    SomethingCreated: [get_something_created_handler]
}

command_handlers: dict[Type[Command], Callable[..., CommandHandler]] = {
    CreateSomething: get_something_creation_handler,
    RaiseException: get_raise_exception_handler,
}


@pytest.mark.asyncio
async def test_messagebus_happy_path(message_bus: MessageBus, capfd):
    # GIVEN
    message_bus.command_handlers = command_handlers
    message_bus.event_handlers = event_handlers

    # WHEN
    res = await message_bus.handle(CreateSomething())

    # THEN
    assert res == "something"
    out, err = capfd.readouterr()
    assert out.strip() == "wow, something was created"


@pytest.mark.asyncio
async def test_messagebus_unhappy_path(message_bus: MessageBus):
    # GIVEN
    message_bus.command_handlers = command_handlers
    message_bus.event_handlers = event_handlers

    # WHEN
    with pytest.raises(ExampleException):
        await message_bus.handle(RaiseException())

    # THEN
    async with message_bus.uow:
        logs: list[FailedMessageLog] = await message_bus.uow.failed_message_log.get_all()
        assert len(logs) == 1
        log = logs[0]
        assert log.message_name == "RaiseException"
        assert log.message_type == "COMMAND"
