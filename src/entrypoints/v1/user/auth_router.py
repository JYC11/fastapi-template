from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette import status

from src.entrypoints.depdencies import AuthServiceDep
from src.entrypoints.v1.user.dto import LoginSuccess, RefreshRequest, RefreshSuccess

auth_router = APIRouter()


@auth_router.get("/login", response_model=LoginSuccess, status_code=status.HTTP_200_OK)
async def login_user(
    auth_service: AuthServiceDep, req: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
):
    token, refresh_token = await auth_service.login(email=req.username, password=req.password)
    return LoginSuccess(token=token, refresh_token=refresh_token)


@auth_router.get("/refresh", response_model=RefreshSuccess, status_code=status.HTTP_200_OK)
async def refresh_token(auth_service: AuthServiceDep, req: Annotated[RefreshRequest, Depends(RefreshRequest)]):
    token = await auth_service.refresh(refresh_token=req.refresh_token, grant_type=req.grant_type)
    return RefreshSuccess(token=token)
