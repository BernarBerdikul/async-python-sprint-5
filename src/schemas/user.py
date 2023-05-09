from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

__all__ = (
    "UserGet",
    "UserCreate",
    "UserUpdate",
)


class UserGet(BaseUser):
    ...


class UserCreate(BaseUserCreate):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "demo@gmail.com",
                "password": "123",
            },
        }


class UserUpdate(BaseUserUpdate):
    ...
