import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import UUIDMixin

__all__ = ("ShortUrlLog",)


class ShortUrlLog(UUIDMixin, SQLModel, table=True):  # type: ignore
    """Short URL log model in database."""

    __tablename__ = "short_url_log"  # noqa

    client: str = Field(nullable=False)
    use_at: datetime = Field(
        title="Datetime of short url usage",
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
        },
    )

    short_url_id: uuid_pkg.UUID = Field(
        title="Short URL ID",
        foreign_key="short_url.id",
        nullable=False,
        index=True,
    )
    short_url: "ShortUrl" = Relationship(  # type: ignore
        back_populates="logs",
    )
