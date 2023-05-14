import http

import pytest
from sqlalchemy import select

from src import settings
from src.models import UserFile


@pytest.mark.asyncio
async def test_get_file_download_url(async_client, async_session, authenticated_user_token):
    jwt_token, active_user = authenticated_user_token
    # create file
    with open("tests/test_file.txt", "rb") as file:
        response = await async_client.post(
            url="/api/v1/files/upload/",
            headers={"Authorization": f"Bearer {jwt_token}"},
            files={"file": file}
        )
        data = response.json()
        file_id = data.pop("id")
        async with async_session() as session:
            result = await session.execute(
                select(UserFile).filter(UserFile.id == file_id)
            )
            instance = result.scalars().first()

    # get files
    response = await async_client.get(
        url=f"/api/v1/files/{file_id}/download/",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.OK, data
    assert data == {
        "url": f"{settings.app.domain}:{settings.minio.port}/{active_user.id}/{instance.path}"
    }
