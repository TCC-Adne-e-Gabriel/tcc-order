from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.main import api_router


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

app.include_router(api_router, prefix=settings.API_V1_STR)

