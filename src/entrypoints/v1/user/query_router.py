from typing import Annotated

from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from starlette import status

from src.domain.user.dto import UserOut, UserSearchParams
from src.entrypoints.depdencies import GetToken, PaginationParamDeps, UserQueryServiceDep
from src.entrypoints.v1.user.dto import UserPaginatedOut
from src.service_layer.exceptions import Forbidden

user_query_router = APIRouter()


@user_query_router.get(
    "/users",
    response_model=UserPaginatedOut,
    status_code=status.HTTP_200_OK,
)
async def paginate_users(
    _: GetToken,
    query_service: UserQueryServiceDep,
    search_params: Annotated[UserSearchParams, Depends(UserSearchParams)],
    pagination_params: PaginationParamDeps,
) -> UserPaginatedOut:
    # TODO: add authorization
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
    token: GetToken,
    user_id: Annotated[str, Path],
    query_service: UserQueryServiceDep,
) -> UserOut:
    if token.sub != user_id:
        raise Forbidden("user id does not match token user id")
    # TODO: add admin authorization
    user: UserOut = await query_service.get_one_or_raise(ident=user_id)
    return user
