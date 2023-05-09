import http

import pytest
from sqlalchemy import select

from src.models import ShortUrl


@pytest.mark.asyncio
async def test_delete_success_short_url(async_client, async_session, short_url_instance):
    response = await async_client.delete(
        url=f"/api/v1/short-urls/{short_url_instance.short_url}/",
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT

    # Get instance from database
    async with async_session() as session:
        result = await session.execute(
            select(ShortUrl).filter(ShortUrl.id == short_url_instance.id)
        )
        instance = result.scalars().first()
    assert instance.is_removed is True

