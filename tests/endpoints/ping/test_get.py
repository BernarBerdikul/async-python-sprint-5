import http

import pytest


@pytest.mark.asyncio
async def test_get_success_ping(async_client):
    response = await async_client.get(url="/ping/")
    data = response.json()
    assert response.status_code == http.HTTPStatus.OK, data
    data.pop("version")
    assert data == {"status": "OK"}
