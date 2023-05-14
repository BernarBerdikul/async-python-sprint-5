import http

from faker import Faker
from sqlalchemy import select

import pytest

from src.models import User


@pytest.mark.asyncio
async def test_user_register(async_client, async_session):
    test_email = Faker().email()
    response = await async_client.post(
        url="/api/v1/auth/register",
        json={
            "email": test_email,
            "password": Faker().password(),
        },
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.CREATED, data

    # Get instance from database
    user_id = data.pop("id")
    async with async_session() as session:
        result = await session.execute(
            select(User).filter(User.id == user_id)
        )
        instance = result.scalars().first()
    assert instance is not None
    assert data == {
        "email": test_email,
        "is_active": instance.is_active,
        "is_superuser": instance.is_superuser,
        "is_verified": instance.is_verified,
    }


@pytest.mark.asyncio
async def test_user_register_empty_body(async_client):
    response = await async_client.post("/api/v1/auth/register")
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_user_register_short_password(async_client):
    response = await async_client.post(
        url="/api/v1/auth/register",
        json={
            "email": Faker().email(),
            "password": "123",
        },
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": {
            "code": "REGISTER_INVALID_PASSWORD",
            "reason": "Password should be at least 8 characters"
        }
    }


@pytest.mark.asyncio
async def test_existed_user_register(async_client, active_user):
    response = await async_client.post(
        url="/api/v1/auth/register",
        json={
            "email": active_user.email,
            "password": "excalibur",
        },
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": "REGISTER_USER_ALREADY_EXISTS"
    }
