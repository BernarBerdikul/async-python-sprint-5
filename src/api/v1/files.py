import http
import uuid as uuid_pkg

from fastapi import APIRouter, Depends, File, UploadFile

from src import settings
from src.models import User
from src.models.user import current_active_user
from src.schemas.user_file import (
    DownloadUserFileLink,
    UserFileItemResponse,
    UserFileListResponse,
)
from src.services import UserFileService, get_user_file_service

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.get(
    path="/",
    response_model=UserFileListResponse,
    summary="Get user's files",
    status_code=http.HTTPStatus.OK,
)
async def get_files(
    user: User = Depends(current_active_user),
    user_file_service: UserFileService = Depends(get_user_file_service),
) -> UserFileListResponse:
    """Get user's files."""
    return await user_file_service.get_all(user_id=user.id)


@router.get(
    path="/{file_id}/download/",
    response_model=DownloadUserFileLink,
    summary="Download file",
    status_code=http.HTTPStatus.OK,
)
async def download_file(
    file_id: uuid_pkg.UUID,
    user: User = Depends(current_active_user),
    user_file_service: UserFileService = Depends(get_user_file_service),
) -> DownloadUserFileLink:
    """Return download file link."""
    user_file = await user_file_service.get(user_id=user.id, file_id=file_id)
    return DownloadUserFileLink(
        url=f"{settings.app.domain}:{settings.minio.port}/{user.id}/{user_file.path}"
    )


@router.post(
    path="/upload/",
    response_model=UserFileItemResponse,
    summary="Upload file",
    status_code=http.HTTPStatus.CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(current_active_user),
    user_file_service: UserFileService = Depends(get_user_file_service),
) -> UserFileItemResponse:
    """Upload file."""
    return await user_file_service.create(user_id=user.id, file=file)
