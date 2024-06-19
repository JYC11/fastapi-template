from typing import Annotated

from fastapi import APIRouter, Body, Path
from starlette import status

from src.domain.models import User
from src.domain.user.commands import CreateUser, DeleteUser, UpdateUser
from src.domain.user.dto import UserOut
from src.entrypoints.depdencies import MessageBusDep
from src.entrypoints.dto import GenericResponse
from src.entrypoints.user.dto import UserCreateIn, UserUpdateIn

router = APIRouter()


@router.post(
    "/user",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    message_bus: MessageBusDep,
    req: UserCreateIn = Body(...),
):
    cmd = CreateUser(email=req.email, phone=req.phone, password=req.password)
    res = await message_bus.handle(message=cmd)
    assert isinstance(res, User)
    return res.to_dto()


@router.put(
    "/user/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def update(
    message_bus: MessageBusDep,
    user_id: Annotated[str, Path],
    req: UserUpdateIn = Body(...),
):
    cmd = UpdateUser(
        id=user_id,
        email=req.email,
        phone=req.phone,
    )
    res = await message_bus.handle(message=cmd)
    assert isinstance(res, User)
    return res.to_dto()


@router.delete(
    "/user/{user_id}",
    response_model=GenericResponse,
    status_code=status.HTTP_200_OK,
)
async def delete(
    message_bus: MessageBusDep,
    user_id: Annotated[str, Path],
):
    cmd = DeleteUser(id=user_id)
    await message_bus.handle(message=cmd)
    return {"success": True}
