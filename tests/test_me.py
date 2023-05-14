import http

import pytest

from src.models import User


@pytest.mark.asyncio
async def test_user_me(async_client, authenticated_user_token: tuple[str, User]):
    jwt_token, active_user = authenticated_user_token
    response = await async_client.get(
        url="/api/v1/users/me",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.OK, data
    assert data == {
        "id": str(active_user.id),
        "email": active_user.email,
        "is_active": active_user.is_active,
        "is_superuser": active_user.is_superuser,
        "is_verified": active_user.is_verified,
    }
