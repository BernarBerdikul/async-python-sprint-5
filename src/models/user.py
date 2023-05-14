import uuid

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
    UUIDIDMixin,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB, SQLModelUserDatabaseAsync
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Relationship

from src import settings
from src.db.db import get_async_session

__all__ = (
    "User",
    "fastapi_users",
    "current_active_user",
    "auth_backend",
)

from src.schemas.user import UserCreate

SECRET = settings.app.jwt_secret


class User(SQLModelBaseUserDB, table=True):
    """User model in database."""

    files: list["UserFile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLModelUserDatabaseAsync(session=session, user_model=User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")


async def get_user_manager(user_db: SQLModelUserDatabaseAsync = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="api/v1/auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET,
        lifetime_seconds=settings.app.jwt_lifetime,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
