from fastapi import APIRouter

from src.models.user import fastapi_users
from src.schemas.user import UserGet, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Add users router
router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserGet,
        user_update_schema=UserUpdate,
    ),
)
