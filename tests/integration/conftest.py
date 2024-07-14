import pytest_asyncio
from argon2 import PasswordHasher
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User
from src.domain.user.dto import UserOut


@pytest_asyncio.fixture
async def create_user(session: AsyncSession, user_data: dict) -> UserOut:
    user = User.create(
        phone=user_data["phone"],
        email=user_data["email"],
        password=user_data["password"],
        hasher=PasswordHasher(),
    )
    session.add(user)
    await session.commit()
    return user.to_dto()


@pytest_asyncio.fixture
async def create_users_for_pagination(session: AsyncSession, user_data: dict) -> list[UserOut]:
    users: list[User] = []
    for _ in range(20):
        user = User.create(
            phone=user_data["phone"],
            email=user_data["email"],
            password=user_data["password"],
            hasher=PasswordHasher(),
        )
        users.append(user)
    session.add_all(users)
    await session.commit()
    return [u.to_dto() for u in users]
