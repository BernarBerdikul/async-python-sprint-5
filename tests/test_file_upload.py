import http

import pytest
from sqlalchemy import select

from src.models import UserFile


@pytest.mark.asyncio
async def test_upload_file(async_client, async_session, authenticated_user_token):
    jwt_token, active_user = authenticated_user_token
    with open("tests/test_file.txt", "rb") as file:
        response = await async_client.post(
            url="/api/v1/files/upload/",
            headers={"Authorization": f"Bearer {jwt_token}"},
            files={"file": file}
        )
    data = response.json()
    assert response.status_code == http.HTTPStatus.CREATED, data

    file_id = data.pop("id")
    async with async_session() as session:
        result = await session.execute(
            select(UserFile).filter(UserFile.id == file_id)
        )
        instance = result.scalars().first()

    assert data == {
        "name": instance.name,
        "path": instance.path,
        "size": instance.size,
        "user_id": str(active_user.id),
        "created_at": instance.created_at.isoformat(),
        "is_downloadable": instance.is_downloadable,
    }
