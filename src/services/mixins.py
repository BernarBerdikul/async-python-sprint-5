from dataclasses import dataclass

from miniopy_async import Minio

from src.repositories import AbstractRepository


@dataclass
class ServiceMixin:
    repository: AbstractRepository
    minio_client: Minio
