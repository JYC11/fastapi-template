import pytest

from src.domain import Command, Event
from src.service.abstract_service import AbstractService
from src.service.exceptions import MethodNotFound


class ExampleService(AbstractService):
    def create_something(self, command: Command) -> str:
        return "something1"

    async def async_create_something(self, command: Command) -> str:
        return "something2"

    def do_something_else(self, event: Event):
        print("event handled 1")

    async def async_do_something_else(self, event: Event):
        print("event handled 2")


@pytest.mark.asyncio
async def test_handles_sync_event_correctly(capfd):
    # GIVEN
    service = ExampleService()

    # WHEN
    await service.handle_event(event=Event(), method_name="do_something_else")

    # THEN
    out, err = capfd.readouterr()
    assert out.strip() == "event handled 1"


@pytest.mark.asyncio
async def test_handles_async_event_correctly(capfd):
    # GIVEN
    service = ExampleService()

    # WHEN
    await service.handle_event(event=Event(), method_name="async_do_something_else")

    # THEN
    out, err = capfd.readouterr()
    assert out.strip() == "event handled 2"


@pytest.mark.asyncio
async def test_handles_sync_command_correctly():
    # GIVEN
    service = ExampleService()

    # WHEN
    res = await service.handle_command(command=Command(), method_name="create_something")

    # THEN
    assert res == "something1"


@pytest.mark.asyncio
async def test_handles_async_command_correctly():
    # GIVEN
    service = ExampleService()

    # WHEN
    res = await service.handle_command(command=Command(), method_name="async_create_something")

    # THEN
    assert res == "something2"


@pytest.mark.asyncio
async def test_raises_exception_when_method_not_found():
    # GIVEN
    service = ExampleService()

    # WHEN
    with pytest.raises(MethodNotFound):  # THEN
        await service.handle_command(command=Command(), method_name="method_doesnt_exist")
