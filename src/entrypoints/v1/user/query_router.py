from typing import Annotated

from fastapi import APIRouter, Path
from starlette import status

from src.domain.models import User
from src.domain.user.dto import UserOut
from src.entrypoints.depdencies import UserQueryServiceDep

user_query_router = APIRouter()


@user_query_router.get(
    "/user/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def get_one_user(
    user_id: Annotated[str, Path],
    query_service: UserQueryServiceDep,
):
    user: User = await query_service.get_one_or_raise(ident=user_id)
    return user.to_dto()
