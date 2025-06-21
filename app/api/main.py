from fastapi import APIRouter

from app.api.routes import order
from app.core.settings import settings

api_router = APIRouter()
api_router.include_router(order.router)

