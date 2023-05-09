import logging
from dataclasses import dataclass
from http import HTTPStatus

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.repositories import ShortUrlRepository
from src.schemas.short_url import (
    ShortUrlBulkCreate,
    ShortUrlCreate,
    ShortUrlDetail,
    ShortUrlFullInfo,
    ShortUrlList,
    ShortUrlShortFullInfo,
)
from src.services import ServiceMixin

__all__ = (
    "ShortUrlService",
    "get_short_url_service",
)

logger = logging.getLogger(__name__)


@dataclass
class ShortUrlService(ServiceMixin):
    """Short url service."""

    async def get(self, short_url: str, request: Request) -> ShortUrlDetail:
        """Get short url by short url."""

        logger.info(f"Getting instance by short url: {short_url}")
        instance = await self.repository.get(short_url=short_url)

        if not instance:
            logger.exception(f"Short url not found: {short_url}")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        elif instance.is_removed:  # type: ignore
            logger.exception(f"Short url is removed: {short_url}")
            raise HTTPException(status_code=HTTPStatus.GONE)

        # If short url is not removed, update usage count
        logger.info(f"Updating usage count for short url: {short_url}")
        await self.repository.update_usage_count(short_url_id=instance.id)

        # Create log record
        client_info = f"{request.client.host}:{request.client.port}"
        logger.info(f"Creating log record for client {client_info}")
        await self.repository.create_log_record(
            short_url_id=instance.id,
            client_info=client_info,
        )
        return ShortUrlDetail.from_orm(instance)

    async def status(
        self,
        short_url: str,
        limit: int,
        offset: int,
        full_info: bool,
    ) -> ShortUrlFullInfo | ShortUrlShortFullInfo:
        """Get short url status."""

        logger.info(f"Getting instance by short url: {short_url}")
        instance = await self.repository.get(short_url=short_url)

        if not instance:
            logger.exception(f"Short url not found: {short_url}")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        elif instance.is_removed:  # type: ignore
            logger.exception(f"Short url is removed: {short_url}")
            raise HTTPException(status_code=HTTPStatus.GONE)

        if not full_info:
            return ShortUrlShortFullInfo.from_orm(instance)

        logs = await self.repository.get_logs(
            short_url_id=instance.id,
            short_url=short_url,
            limit=limit,
            offset=offset,
            full_info=full_info,
        )
        return ShortUrlFullInfo(
            id=instance.id,
            short_url=instance.short_url,
            original_url=instance.original_url,
            usage_count=instance.usage_count,
            logs=logs,
        )

    async def create(self, data: ShortUrlCreate) -> ShortUrlDetail:
        """Create short url."""
        logger.info(f"Creating short url: {data}")
        return ShortUrlDetail.from_orm(await self.repository.add(data=data))

    async def bulk_create(self, data: ShortUrlBulkCreate) -> ShortUrlList:
        """Create short urls."""
        logger.info(f"Bulk creating short urls: {data}")
        return ShortUrlList.from_orm(await self.repository.bulk_add(data=data))

    async def delete(self, short_url: str) -> None:
        """Soft delete short url."""
        logger.info(f"Soft deleting short url: {short_url}")
        await self.repository.delete(short_url=short_url)


async def get_short_url_service(
    session: AsyncSession = Depends(get_async_session),
) -> ShortUrlService:
    """Get short url service."""
    repository = ShortUrlRepository(session=session)
    return ShortUrlService(repository=repository)
