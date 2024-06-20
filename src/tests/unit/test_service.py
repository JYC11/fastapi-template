from typing import Any

import pytest

from src.domain import Command, Event
from src.service_layer.abstracts.abstract_service import AbstractService
from src.service_layer.exceptions import MethodNotFound


class ExampleService(AbstractService):

    def sync_create(self, command: Command) -> str:
        return "something1"

    async def create(self, command: Command) -> str:
        return "something2"

    def do_something_else(self, event: Event):
        print("event handled 1")

    async def async_do_something_else(self, event: Event):
        print("event handled 2")

    async def update(self, cmd: Any):
        pass

    async def delete(self, cmd: Any):
        pass


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
    res = await service.handle_command(command=Command(), method_name="sync_create")

    # THEN
    assert res == "something1"


@pytest.mark.asyncio
async def test_handles_async_command_correctly():
    # GIVEN
    service = ExampleService()

    # WHEN
    res = await service.handle_command(command=Command(), method_name="create")

    # THEN
    assert res == "something2"


@pytest.mark.asyncio
async def test_raises_exception_when_method_not_found():
    # GIVEN
    service = ExampleService()

    # WHEN
    with pytest.raises(MethodNotFound):  # THEN
        await service.handle_command(command=Command(), method_name="method_doesnt_exist")
