from fastapi import APIRouter

from src.models.user import auth_backend, fastapi_users
from src.schemas.user import UserCreate, UserGet

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# Add basic routers for authentication
router.include_router(
    fastapi_users.get_auth_router(
        backend=auth_backend,
    ),
)
router.include_router(
    fastapi_users.get_register_router(
        user_schema=UserGet,
        user_create_schema=UserCreate,
    ),
)
router.include_router(
    fastapi_users.get_verify_router(
        user_schema=UserGet,
    ),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)
