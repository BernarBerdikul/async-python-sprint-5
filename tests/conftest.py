import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from faker import Faker
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db import async_engine
from src.main import app
from src.models import User


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    yield session
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def active_user(async_session) -> User:
    password_helper = PasswordHelper()
    test_email = Faker().email()
    async with async_session() as session:
        user = User(
            email=test_email,
            hashed_password=password_helper.hash("excalibur"),
        )
        session.add(user)
        await session.commit()
    yield user


@pytest_asyncio.fixture(scope="function")
async def authenticated_user_token(async_client, active_user) -> tuple[str, User]:
    response = await async_client.post(
        url="/api/v1/auth/login",
        data={
            "username": active_user.email,
            "password": "excalibur",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = response.json()
    yield data.pop("access_token"), active_user
