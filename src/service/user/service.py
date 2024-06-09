from src.service.abstract_unit_of_work import AbstractUnitOfWork


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def create(self):
        return  # TODO

    def update(self):
        return  # TODO

    def delete(self):
        return  # TODO
