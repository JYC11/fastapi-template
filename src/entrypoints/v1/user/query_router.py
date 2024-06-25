from typing import Annotated

from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from starlette import status

from src.domain.models import User
from src.domain.user.dto import UserOut, UserSearchParams
from src.entrypoints.depdencies import PaginationParamDeps, UserQueryServiceDep
from src.entrypoints.v1.user.dto import UserPaginatedOut

user_query_router = APIRouter()


@user_query_router.get("/users", response_model=UserPaginatedOut, status_code=status.HTTP_200_OK)
async def paginate_users(
    query_service: UserQueryServiceDep,
    search_params: Annotated[UserSearchParams, Depends(UserSearchParams)],
    pagination_params: PaginationParamDeps,
):
    users, total = await query_service.paginate(
        search_params=search_params,
        pagination_params=pagination_params,
    )
    return UserPaginatedOut(
        items=users,
        total=total,
        page=pagination_params.page,
        size=pagination_params.size,
    )


@user_query_router.get(
    "/users/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def get_one_user(
    user_id: Annotated[str, Path],
    query_service: UserQueryServiceDep,
):
    user: User = await query_service.get_one_or_raise(ident=user_id)
    return user.to_dto()
