import http

import pytest
from sqlalchemy import select

from src.models import ShortUrlLog
from tests.factories.short_url import ShortUrlFactory


@pytest.mark.asyncio
async def test_get_short_url_full_info(async_client, async_session, short_url_instance):
    full_info = "true"
    limit = 10
    offset = 0
    response = await async_client.get(
        url=f"/api/v1/short-urls/{short_url_instance.short_url}/status/?full-info={full_info}&max-size={limit}&offset={offset}"
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.OK, data

    async with async_session() as session:
        # Get logs from database
        result = await session.execute(
            select(ShortUrlLog)
            .where(
                ShortUrlLog.short_url_id == short_url_instance.id,
            )
            .order_by(ShortUrlLog.use_at.desc())
            .limit(limit)
            .offset(offset)
        )
        logs = result.scalars().all()
    assert data == {
        "id": str(short_url_instance.id),
        "short_url": short_url_instance.short_url,
        "original_url": short_url_instance.original_url,
        "usage_count": short_url_instance.usage_count,
        "logs": [
            {
                "id": str(log.id),
                "use_at": log.use_at.isoformat(),
            }
            for log in logs
        ]
    }


@pytest.mark.asyncio
async def test_get_short_url_short_full_info(async_client, short_url_instance):
    limit = 10
    offset = 0
    response = await async_client.get(
        url=f"/api/v1/short-urls/{short_url_instance.short_url}/status/?max-size={limit}&offset={offset}"
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.OK, data
    assert data == {
        "id": str(short_url_instance.id),
        "short_url": short_url_instance.short_url,
        "original_url": short_url_instance.original_url,
        "usage_count": short_url_instance.usage_count,
    }


@pytest.mark.asyncio
async def test_get_short_url_status_not_found(async_client):
    short_url_instance = ShortUrlFactory()
    response = await async_client.get(
        url=f"/api/v1/short-urls/{short_url_instance.short_url}/status/"
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.NOT_FOUND, data
    assert data == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_get_short_url_status_removed(async_client, removed_short_url_instance):
    response = await async_client.get(
        url=f"/api/v1/short-urls/{removed_short_url_instance.short_url}/status/"
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.GONE, data
    assert data == {"detail": "Gone"}
