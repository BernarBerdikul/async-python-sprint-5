from miniopy_async import Minio

from src import settings

minio_client = Minio(
    endpoint=f"{settings.minio.host}:{settings.minio.port}",
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    secure=False,
)


async def get_minio_client() -> Minio:
    yield minio_client
