import uuid as uuid_pkg
from datetime import datetime

from pydantic import HttpUrl

from src.schemas.base import FastORMJsonModel

__all__ = (
    "ShortUrlCreate",
    "ShortUrlBulkCreate",
    "ShortUrlDetail",
    "ShortUrlList",
    "ShortUrlShortFullInfo",
    "ShortUrlFullInfo",
)


class ShortUrlCreate(FastORMJsonModel):
    """Short URL create model."""

    original_url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "original_url": "https://www.google.com/",
            },
        }


class ShortUrlBulkCreate(FastORMJsonModel):
    """Short URL bulk create model."""

    urls: list[HttpUrl]

    class Config:
        schema_extra = {
            "example": {
                "urls": [
                    "https://www.google.com/",
                    "https://www.yandex.ru/",
                ],
            },
        }


class ShortUrlDetail(FastORMJsonModel):
    """Short URL detail model."""

    id: uuid_pkg.UUID
    short_url: str
    original_url: HttpUrl


class ShortUrlShortFullInfo(ShortUrlDetail):
    """Short URL short full info model."""

    usage_count: int


class ShortUrlLogRead(FastORMJsonModel):
    """Short URL log read model."""

    id: uuid_pkg.UUID
    client: str
    use_at: datetime


class ShortUrlFullInfo(ShortUrlShortFullInfo):
    """Short URL full info model."""

    logs: list[ShortUrlLogRead]


class ShortUrlList(FastORMJsonModel):
    """Short URL list model."""

    __root__: list[ShortUrlDetail]
