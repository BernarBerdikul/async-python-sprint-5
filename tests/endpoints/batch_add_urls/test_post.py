import http

import pytest


@pytest.mark.asyncio
async def test_bulk_create_success_short_url(async_client):
    urls = [
        "https://www.google.com/",
        "https://www.yandex.ru/",
    ]
    response = await async_client.post(
        url="/api/v1/short-urls/batch-add-urls/",
        json={"urls": urls},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.CREATED, data
    assert len(data) == len(urls)
