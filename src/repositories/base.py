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
    async def get(self, *args, **kwargs) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, *args, **kwargs) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError
