import http

import pytest
from sqlalchemy import select

from src.models import ShortUrlLog, ShortUrl
from tests.factories.short_url import ShortUrlFactory


@pytest.mark.asyncio
async def test_get_short_url(async_client, async_session, short_url_instance):
    old_usage_count = short_url_instance.usage_count
    response = await async_client.get(
        url=f"/api/v1/short-urls/{short_url_instance.short_url}/"
    )
    assert response.status_code == http.HTTPStatus.TEMPORARY_REDIRECT

    async with async_session() as session:
        # Get logs from database
        result = await session.execute(
            select(ShortUrlLog)
            .where(
                ShortUrlLog.short_url_id == short_url_instance.id,
            )
        )
        logs = result.scalars().all()
        # Get instance from database
        result = await session.execute(
            select(ShortUrl).filter(ShortUrl.id == short_url_instance.id)
        )
        instance = result.scalars().first()
    assert len(logs) == 1
    assert old_usage_count != instance.usage_count


@pytest.mark.asyncio
async def test_get_short_url_not_found(async_client):
    short_url_instance = ShortUrlFactory()
    response = await async_client.get(
        url=f"/api/v1/short-urls/{short_url_instance.short_url}/"
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.NOT_FOUND, data
    assert data == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_get_short_url_removed(async_client, removed_short_url_instance):
    response = await async_client.get(
        url=f"/api/v1/short-urls/{removed_short_url_instance.short_url}/"
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.GONE, data
    assert data == {"detail": "Gone"}
