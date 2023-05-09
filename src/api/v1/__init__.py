from fastapi import APIRouter
from .short_urls import router as short_urls_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(short_urls_router)
