from pydantic import BaseModel


class GenericResponse(BaseModel):
    success: bool
