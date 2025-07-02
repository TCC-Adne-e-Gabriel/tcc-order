from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.main import api_router
from fastapi import Request
from http import HTTPStatus
from .exceptions import AppException
from fastapi.responses import JSONResponse


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

@app.exception_handler(AppException)
async def user_not_found_exception_handler(request: Request, exc: AppException): 
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": f"{exc.detail}"}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"detail": "Ocorreu um erro inesperado."}
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

