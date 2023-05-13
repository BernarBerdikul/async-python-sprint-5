import logging
import uuid as uuid_pkg
from dataclasses import dataclass
from http import HTTPStatus

from fastapi import Depends, File, HTTPException
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.db.minio import get_minio_client
from src.repositories import UserFileRepository
from src.schemas.user_file import (
    UserFileCreate,
    UserFileItemResponse,
    UserFileListResponse,
)
from src.services import ServiceMixin

__all__ = (
    "UserFileService",
    "get_user_file_service",
)

logger = logging.getLogger(__name__)


@dataclass
class UserFileService(ServiceMixin):
    """User file service."""

    async def get(
        self, user_id: uuid_pkg.UUID, file_id: uuid_pkg.UUID
    ) -> UserFileItemResponse:
        """Get user file."""
        user_file = await self.repository.get(user_id=user_id, file_id=file_id)
        if not user_file:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User file not found: {file_id}",
            )
        return UserFileItemResponse.from_orm(user_file)

    async def get_all(self, user_id: uuid_pkg.UUID) -> UserFileListResponse:
        """Get all user files."""
        logger.info(f"Getting all user files for user: {user_id}")
        files = await self.repository.all(user_id=user_id)
        return UserFileListResponse(
            user_id=user_id,
            files=files,
        )

    async def create(self, user_id: uuid_pkg.UUID, file: File) -> UserFileItemResponse:
        """Create short url."""
        bucket_name = f"{user_id}"
        path = f"files/{file.filename.replace(' ', '_')}"
        # Create bucket if not exists
        if not await self.minio_client.bucket_exists(bucket_name):
            await self.minio_client.make_bucket(bucket_name)

        # Save the uploaded file to Minio
        await self.minio_client.put_object(
            bucket_name=bucket_name,
            object_name=path,
            data=file.file,
            length=file.size,
        )

        data = UserFileCreate(
            user_id=user_id,
            name=file.filename,
            path=path,
            size=file.size,
        )
        logger.info(f"Creating user file: {data}")
        return UserFileItemResponse.from_orm(
            await self.repository.add(data=data),
        )


async def get_user_file_service(
    session: AsyncSession = Depends(get_async_session),
    minio_client: Minio = Depends(get_minio_client),
) -> UserFileService:
    """Get user file service."""
    return UserFileService(
        repository=UserFileRepository(session=session),
        minio_client=minio_client,
    )
