import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel

__all__ = (
    "UUIDMixin",
    "CreatedAtMixin",
)


class UUIDMixin(SQLModel):
    id: uuid_pkg.UUID = Field(
        title="Уникальный идентификатор объекта",
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
            "unique": True,
        },
    )


class CreatedAtMixin(UUIDMixin):
    created_at: datetime = Field(
        title="Время создания объекта",
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
        },
    )
