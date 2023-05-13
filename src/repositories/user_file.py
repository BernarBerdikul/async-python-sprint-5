import uuid as uuid_pkg

from sqlalchemy import select

from src.models import UserFile
from src.repositories import AbstractRepository
from src.schemas.user_file import UserFileCreate

__all__ = ("UserFileRepository",)


class UserFileRepository(AbstractRepository):
    """User file repository."""

    model: type[UserFile] = UserFile

    async def get(
        self, user_id: uuid_pkg.UUID, file_id: uuid_pkg.UUID
    ) -> UserFile | None:
        """Get user file."""
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == file_id,
                self.model.user_id == user_id,
            )
        )
        return result.scalars().first()

    async def all(self, user_id: uuid_pkg.UUID) -> list[UserFile]:
        """Get all user files."""
        result = await self.session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
            )
        )
        return result.scalars().all()

    async def add(self, data: UserFileCreate) -> UserFile:
        """Add user file."""
        new_user_file = self.model.from_orm(data)
        self.session.add(new_user_file)
        await self.session.commit()
        await self.session.refresh(new_user_file)
        return new_user_file
