from typing import Annotated

from fastapi import APIRouter, Body, Path
from starlette import status

from src.domain.models import User
from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.dto import UserOut
from src.entrypoints.depdencies import MessageBusDep
from src.entrypoints.dto import GenericResponse
from src.entrypoints.v1.user.dto import UserCreateIn, UserUpdateIn

user_command_router = APIRouter()


@user_command_router.post(
    "/user",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    message_bus: MessageBusDep,
    req: Annotated[UserCreateIn, Body()],
):
    cmd = CreateUser(email=req.email, phone=req.phone, password=req.password)
    res = await message_bus.handle(message=cmd)
    assert isinstance(res, User)
    return res.to_dto()


@user_command_router.put(
    "/user/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    message_bus: MessageBusDep,
    user_id: Annotated[str, Path],
    req: Annotated[UserUpdateIn, Body()],
):
    cmd = UpdateUser(
        id=user_id,
        email=req.email,
        phone=req.phone,
    )
    res = await message_bus.handle(message=cmd)
    assert isinstance(res, User)
    return res.to_dto()


@user_command_router.delete(
    "/user/{user_id}",
    response_model=GenericResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    message_bus: MessageBusDep,
    user_id: Annotated[str, Path],
):
    cmd = DeleteUser(id=user_id)
    await message_bus.handle(message=cmd)
    return {"success": True}
