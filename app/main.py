from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.main import api_router
from fastapi import Request
from http import HTTPStatus
from .exceptions import AppException
from fastapi.responses import JSONResponse
from app.context import user_id_context
from app.order_logging import logger
from uuid import uuid4
from app.middlewares import ClientIPMiddleware


app = FastAPI(
    title="tcc-order",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ClientIPMiddleware)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException): 
    logger.error(f"{exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": f"{exc.detail}"}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_code = str(uuid4())[:8]
    logger.error(f"{error_code}: ", exc_info=exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content = {
            "detail": f"{error_code} - An unexpected error occurred. Please report the error code to support.",
            "error_code": error_code,
        }
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

