from src.service.abstract_service import AbstractService
from src.service.abstract_unit_of_work import AbstractUnitOfWork


class UserService(AbstractService):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(self):
        return  # TODO

    async def update(self):
        return  # TODO

    async def delete(self):
        return  # TODO
