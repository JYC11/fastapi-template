# TODO add error messages


class ItemNotFound(Exception): ...


class MethodNotFound(Exception): ...


class Unauthorized(Exception): ...


class Forbidden(Exception): ...


class DuplicateRecord(Exception): ...


class ConcurrencyException(Exception): ...