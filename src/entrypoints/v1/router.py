from fastapi import APIRouter

from src.common.settings import settings
from src.entrypoints.v1.user.authentication_router import auth_router
from src.entrypoints.v1.user.command_router import user_command_router
from src.entrypoints.v1.user.query_router import user_query_router

api_v1_router = APIRouter()

api_v1_router.include_router(user_query_router, prefix=settings.api_v1_str)
api_v1_router.include_router(user_command_router, prefix=settings.api_v1_str)
api_v1_router.include_router(auth_router, prefix=settings.api_v1_str)
