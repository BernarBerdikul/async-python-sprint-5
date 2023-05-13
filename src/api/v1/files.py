from fastapi import APIRouter, Depends, File, UploadFile

from src.db.minio import get_minio_client

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


# @router.get(
#     path="/",
#     response_model=ShortUrlDetail,
#     summary="Get user's files",
#     status_code=http.HTTPStatus.OK,
# )
# async def create_short_url(
#     *,
#     data: ShortUrlCreate,
#     short_url_service: ShortUrlService = Depends(get_short_url_service),
# ) -> ShortUrlDetail:
#     """Create short url."""
#     return await short_url_service.create(data=data)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    minio_client=Depends(get_minio_client),
):
    # Create bucket
    await minio_client.make_bucket("my-bucket")
    # Save the uploaded file to Minio
    await minio_client.put_object(
        bucket_name="my-bucket",
        object_name=file.filename,
        data=file.file,
        length=file.size,
    )
    return {"message": "File uploaded successfully"}
