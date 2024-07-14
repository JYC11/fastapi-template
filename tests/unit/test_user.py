from argon2 import PasswordHasher

from src.domain.models import User


def test_create_user():
    # WHEN
    user = User.create(
        phone="010",
        email="email@email.com",
        password="password",
        hasher=PasswordHasher(),
    )

    # THEN
    assert isinstance(user, User)
    assert user.password != "password"


def test_verify_password_happy_path():
    # WHEN
    user = User.create(
        phone="010",
        email="email@email.com",
        password="password",
        hasher=PasswordHasher(),
    )

    # THEN
    assert isinstance(user, User)
    assert user.verify(password="password", hasher=PasswordHasher())


def test_verify_password_unhappy_path():
    # WHEN
    user = User.create(
        phone="010",
        email="email@email.com",
        password="password",
        hasher=PasswordHasher(),
    )

    # THEN
    assert isinstance(user, User)
    assert not user.verify(password="not password", hasher=PasswordHasher())


def test_update_user_password():
    # GIVEN
    user = User.create(
        phone="010",
        email="email@email.com",
        password="password",
        hasher=PasswordHasher(),
    )
    assert isinstance(user, User)

    # WHEN
    user.update_password(password="new password", hasher=PasswordHasher())

    # THEN
    assert user.verify(password="new password", hasher=PasswordHasher())
