from fastapi import APIRouter
from .auth import router as auth_router
from .files import router as files_router
from .users import router as users_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(files_router)
api_v1_router.include_router(users_router)
