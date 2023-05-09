import http

from fastapi import APIRouter, Depends, Request
from fastapi.params import Query
from fastapi.responses import ORJSONResponse

from src.schemas.short_url import (
    ShortUrlBulkCreate,
    ShortUrlCreate,
    ShortUrlDetail,
    ShortUrlFullInfo,
    ShortUrlList,
    ShortUrlShortFullInfo,
)
from src.services import ShortUrlService, get_short_url_service

router = APIRouter(
    prefix="/short-urls",
    tags=["short-urls"],
)


@router.post(
    path="/",
    response_model=ShortUrlDetail,
    summary="Create short url",
    status_code=http.HTTPStatus.CREATED,
)
async def create_short_url(
    *,
    data: ShortUrlCreate,
    short_url_service: ShortUrlService = Depends(get_short_url_service),
) -> ShortUrlDetail:
    """Create short url."""
    return await short_url_service.create(data=data)


@router.post(
    path="/batch-add-urls/",
    response_model=ShortUrlList,
    summary="Create multiple short urls",
    status_code=http.HTTPStatus.CREATED,
)
async def create_short_urls(
    *,
    data: ShortUrlBulkCreate,
    short_url_service: ShortUrlService = Depends(get_short_url_service),
) -> ShortUrlList:
    """Create multiple short urls."""
    return await short_url_service.bulk_create(data=data)


@router.delete(
    path="/{short_url}/",
    response_model=None,
    summary="Delete short url",
    status_code=http.HTTPStatus.NO_CONTENT,
)
async def delete_short_url(
    *,
    short_url: str,
    short_url_service: ShortUrlService = Depends(get_short_url_service),
):
    """Delete short url."""
    await short_url_service.delete(short_url=short_url)
    return ORJSONResponse(content=None, status_code=http.HTTPStatus.NO_CONTENT)


@router.get(
    path="/{short_url}/",
    summary="Get short url",
    status_code=http.HTTPStatus.TEMPORARY_REDIRECT,
)
async def get_short_url_detail(
    *,
    short_url: str,
    request: Request,
    short_url_service: ShortUrlService = Depends(get_short_url_service),
):
    """Get short url."""
    result: ShortUrlDetail = await short_url_service.get(
        short_url=short_url, request=request
    )
    data = {"detail": "Temporary Redirect", "location": result.original_url}
    return ORJSONResponse(
        content=data,
        status_code=http.HTTPStatus.TEMPORARY_REDIRECT,
        headers={"Location": result.original_url},
    )


@router.get(
    path="/{short_url}/status/",
    summary="Get short url status",
    status_code=http.HTTPStatus.OK,
)
async def get_short_url_status(
    *,
    short_url: str,
    full_info: bool = Query(default=False, alias="full-info"),
    limit: int = Query(
        default=10, ge=1, alias="max-size", description="Query max size."
    ),
    offset: int = Query(default=0, ge=0, description="Query offset."),
    short_url_service: ShortUrlService = Depends(get_short_url_service),
) -> ShortUrlFullInfo | ShortUrlShortFullInfo:
    """Get short url status."""
    return await short_url_service.status(
        short_url=short_url,
        full_info=full_info,
        limit=limit,
        offset=offset,
    )
