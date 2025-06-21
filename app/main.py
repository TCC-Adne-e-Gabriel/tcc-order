from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.core.settings import settings
from app.api.main import api_router
from app.initial_data import initialize_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando tabelas do banco de dados.")
    initialize_db()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="tcc-order",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

