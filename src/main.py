import http

import sqlalchemy as sa
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from src import settings
from src.api.v1 import api_v1_router
from src.db.db import get_async_session
from src.middlewares import add_process_time_header


def create_app() -> FastAPI:
    current_app = FastAPI(
        title=settings.app.project_name,
        description=settings.app.description,
        version=settings.app.version,
        # OpenAPI interface address
        docs_url="/api/openapi",
        redoc_url="/api/redoc",
        # OpenAPI docs address
        openapi_url=f"{settings.app.api_doc_prefix}/openapi.json",
        debug=settings.app.debug,
        default_response_class=ORJSONResponse,
        authenticated_route=["authenticated-route"],
    )
    # Middlewares
    current_app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)

    # Routers
    current_app.include_router(api_v1_router)
    return current_app


app = create_app()


@app.get(path="/ping/", status_code=http.HTTPStatus.OK, tags=["status"])
async def ping(session: AsyncSession = Depends(get_async_session)):
    try:
        # Выполните любой запрос, чтобы проверить доступность БД
        result = await session.scalar(sa.select(sa.text("version();")))
        return {"status": "OK", "version": result}
    except (OperationalError, DatabaseError) as e:
        return HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={"status": "ERROR", "detail": str(e)},
        )


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )
