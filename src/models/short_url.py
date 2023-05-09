from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import UUIDMixin

__all__ = ("ShortUrl",)


class ShortUrl(UUIDMixin, SQLModel, table=True):  # type: ignore
    """Short URL model in database."""

    __tablename__ = "short_url"  # noqa

    short_url: str = Field(
        nullable=False,
        unique=True,
        index=True,
    )
    original_url: str = Field(nullable=False)
    usage_count: int = Field(
        title="Short URL usage count",
        default=0,
        nullable=False,
    )
    is_removed: bool = Field(
        title="Deleted flag",
        default=False,
        nullable=False,
    )
    logs: list["ShortUrlLog"] = Relationship(  # type: ignore
        back_populates="short_url",
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )
