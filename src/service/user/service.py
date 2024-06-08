

from src.service.abstract_unit_of_work import AbstractUnitOfWork


class UserService:
    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self.unit_of_work = unit_of_work

    def create(self):
        return  # TODO

    def update(self):
        return  # TODO

    def delete(self):
        return  # TODO
