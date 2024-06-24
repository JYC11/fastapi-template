from typing import Any

from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import nullslast

from src.entrypoints.exceptions import InvalidSortException


class GenericResponse(BaseModel):
    success: bool


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)
    sort: str | None = Field(None)

    @property
    def offset(self):
        return self.size * (self.page - 1)

    def paginate(self, query: Select):
        return query.offset(self.offset).limit(self.size)

    def parse_order_by_conditions(self):
        assert self.sort is not None
        return self.sort.replace(" ", "").split(",")

    def get_order_by_conditions(self, model, skip_columns: list[str] | None = None) -> list:
        if not self.sort:
            return []
        ordering = []
        conditions = self.parse_order_by_conditions()
        for condition in conditions:
            asc = True
            if condition.startswith("-"):
                asc = False
                condition = condition[1:]
            if skip_columns and condition in skip_columns:
                continue
            if hasattr(model, condition):
                order_column = getattr(model, condition)
                ordering.append(nullslast(order_column.asc()) if asc else nullslast(order_column.desc()))
            else:
                raise InvalidSortException(f"invalid sorting parameter: {condition}")
        return ordering


class PaginationOut(BaseModel):
    items: list[Any] = Field([])
    total: int = Field(0, ge=0)
    page: int = Field(0, ge=0)
    size: int = Field(5, ge=1, le=100)
