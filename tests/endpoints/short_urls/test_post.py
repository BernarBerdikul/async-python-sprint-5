import http

import pytest
from sqlalchemy import select

from src.models import ShortUrl


@pytest.mark.asyncio
async def test_create_success_short_url(async_client, async_session):
    response = await async_client.post(
        url="/api/v1/short-urls/",
        json={"original_url": "https://www.google.com/"},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.CREATED, data

    # Get instance from database
    async with async_session() as session:
        result = await session.execute(
            select(ShortUrl).filter(ShortUrl.id == data["id"])
        )
        instance = result.scalars().first()
    assert instance is not None
