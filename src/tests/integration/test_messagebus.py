from typing import Any, Callable, Type

import pytest
from sqlalchemy.ext.asyncio import async_scoped_session

from src.domain import Command, Event
from src.domain.models import FailedMessageLog
from src.service_layer.abstracts.abstract_service import AbstractService
from src.service_layer.abstracts.abstract_unit_of_work import AbstractUnitOfWork
from src.service_layer.message_bus import MessageBus
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork


class CreateSomething(Command): ...


class RaiseException(Command): ...


class SomethingCreated(Event):
    message: str


class ExampleException(Exception): ...


class ExampleService(AbstractService):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(self, command: CreateSomething) -> str:
        self.uow.events.append(SomethingCreated(message="wow"))
        return "something"

    def do_something_else(self, event: SomethingCreated):
        print(f"{event.message}, something was created")

    def raise_exception(self, command: RaiseException):
        raise ExampleException()

    async def update(self, cmd: Any):
        pass

    async def delete(self, cmd: Any):
        pass


class fake_async_scoped_session(async_scoped_session):
    def __init__(self): ...


def get_example_service() -> AbstractService:
    return ExampleService(
        uow=SqlAlchemyUnitOfWork(
            session_factory=fake_async_scoped_session,
            repositories=dict(),
        )
    )


event_handlers: dict[Type[Event], list[tuple[Callable[..., AbstractService], str]]] = {
    SomethingCreated: [(get_example_service, "do_something_else")]
}

command_handlers: dict[Type[Command], tuple[Callable[..., AbstractService], str]] = {
    CreateSomething: (get_example_service, "create"),
    RaiseException: (get_example_service, "raise_exception"),
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
    await message_bus.handle(RaiseException())

    # THEN
    async with message_bus.uow:
        logs: list[FailedMessageLog] = await message_bus.uow.failed_message_log.list()
        assert len(logs) == 1
        log = logs[0]
        assert log.message_name == "RaiseException"
        assert log.message_type == "COMMAND"
