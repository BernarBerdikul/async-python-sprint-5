import uuid

from sqlalchemy import select, update

from src.models import ShortUrl, ShortUrlLog
from src.repositories import AbstractRepository
from src.schemas.short_url import ShortUrlBulkCreate, ShortUrlCreate
from src.utils import shortuuid

__all__ = ("ShortUrlRepository",)


class ShortUrlRepository(AbstractRepository):
    model: type[ShortUrl] = ShortUrl  # type: ignore

    async def get(self, short_url: str) -> ShortUrl | None:  # type: ignore
        """Get short url by short url."""
        result = await self.session.execute(
            select(self.model).where(
                self.model.short_url == short_url,
            )
        )
        return result.scalars().first()

    async def add(self, data: ShortUrlCreate) -> ShortUrl:
        """Add short url."""
        new_short_url = self.model(
            short_url=await shortuuid.uuid(),
            original_url=data.original_url,
        )
        self.session.add(new_short_url)
        await self.session.commit()
        await self.session.refresh(new_short_url)
        return new_short_url

    async def bulk_add(self, data: ShortUrlBulkCreate) -> list[ShortUrl]:
        """Bulk add short urls."""
        new_short_urls = [
            self.model(
                short_url=await shortuuid.uuid(),
                original_url=url,
            )
            for url in data.urls
        ]
        self.session.add_all(new_short_urls)
        await self.session.commit()
        return new_short_urls

    async def delete(self, short_url: str) -> None:
        """Soft delete short url."""
        await self.session.execute(
            update(self.model)
            .where(self.model.short_url == short_url)
            .values(is_removed=True)
        )
        await self.session.commit()

    async def update_usage_count(self, short_url_id: uuid.UUID) -> None:
        """Update usage count."""
        await self.session.execute(
            update(self.model)
            .where(self.model.id == short_url_id)
            .values(usage_count=self.model.usage_count + 1)
        )
        await self.session.commit()

    async def create_log_record(
        self, short_url_id: uuid.UUID, client_info: str
    ) -> None:
        """Create log record."""
        short_url_log = ShortUrlLog(
            short_url_id=short_url_id,
            client=client_info,
        )
        self.session.add(short_url_log)
        await self.session.commit()

    async def get_logs(
        self,
        short_url_id: uuid.UUID,
        short_url: str,
        limit: int,
        offset: int,
        full_info: bool,
    ) -> list[ShortUrlLog]:
        """Get short url logs."""
        result = await self.session.execute(
            select(ShortUrlLog)
            .where(
                ShortUrlLog.short_url_id == short_url_id,
            )
            .order_by(ShortUrlLog.use_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
