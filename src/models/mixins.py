import uuid as uuid_pkg

from sqlalchemy import text
from sqlmodel import Field, SQLModel

__all__ = ("UUIDMixin",)


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
