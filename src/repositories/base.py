from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

__all__ = ("AbstractRepository",)

ModelType = TypeVar("ModelType", bound=SQLModel)


@dataclass
class AbstractRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def get(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def add(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def bulk_add(self, *args, **kwargs) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_usage_count(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_log_record(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_logs(self, *args, **kwargs) -> list[ModelType]:
        raise NotImplementedError
