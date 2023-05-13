import uuid as uuid_pkg

from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import CreatedAtMixin

__all__ = ("UserFile",)


class UserFile(CreatedAtMixin, SQLModel, table=True):
    """User file model in database."""

    __tablename__ = "user_file"

    name: str = Field(max_length=100, nullable=False)
    path: str = Field(max_length=256, nullable=False)
    size: int = Field(nullable=False)
    is_downloadable: bool = Field(
        nullable=False,
        default=True,
    )

    user_id: uuid_pkg.UUID = Field(
        title="User ID",
        foreign_key="user.id",
        nullable=False,
        index=True,
    )
    user: "User" = Relationship(back_populates="files")
