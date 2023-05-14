import http

from faker import Faker

import pytest


@pytest.mark.asyncio
async def test_user_login(async_client, active_user):
    response = await async_client.post(
        url="/api/v1/auth/login",
        data={
            "username": active_user.email,
            "password": "excalibur",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.OK, data
    assert data.pop("access_token") is not None
    assert data == {"token_type": "bearer"}


@pytest.mark.asyncio
async def test_user_login_empty_data(async_client):
    response = await async_client.post(
        url="/api/v1/auth/login",
        data={},
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_nonuser_login(async_client):
    response = await async_client.post(
        url="/api/v1/auth/login",
        data={
            "username": Faker().email(),
            "password": Faker().password(),
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.BAD_REQUEST, data
    assert data == {
        "detail": "LOGIN_BAD_CREDENTIALS",
    }
