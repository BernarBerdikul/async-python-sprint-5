import uuid as uuid_pkg
from datetime import datetime

from .base import FastORMJsonModel

__all__ = (
    "DownloadUserFileLink",
    "UserFileCreate",
    "UserFileItemResponse",
    "UserFileListResponse",
)


class DownloadUserFileLink(FastORMJsonModel):
    """Download user file link schema."""

    url: str


class UserFileBase(FastORMJsonModel):
    """User file base schema."""

    name: str
    path: str
    size: int


class UserFileCreate(UserFileBase):
    """User file create schema."""

    user_id: uuid_pkg.UUID


class UserFileItemResponse(UserFileCreate):
    """User file item response schema."""

    id: uuid_pkg.UUID
    created_at: datetime
    is_downloadable: bool


class UserFileListResponse(FastORMJsonModel):
    """User file list response schema."""

    user_id: uuid_pkg.UUID
    files: list[UserFileItemResponse]
