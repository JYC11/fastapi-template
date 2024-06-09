import abc
import inspect

from typing_extensions import Callable

from src.domain import Command, Event, Message
from src.service.abstract_unit_of_work import AbstractUnitOfWork


def method_not_found(message: Message):
    return  # TODO raise exception


class AbstractService(abc.ABC):
    uow: AbstractUnitOfWork

    async def handle_command(self, method_name: str, command: Command):
        func: Callable = getattr(self, method_name, method_not_found)
        task = func(command)  # type: ignore
        if inspect.isawaitable(task):
            res = await task
        else:
            res = task
        return res

    async def handle_event(self, method_name: str, event: Event):
        func: Callable = getattr(self, method_name, method_not_found)
        task = func(event)  # type: ignore
        if inspect.isawaitable(task):
            await task
