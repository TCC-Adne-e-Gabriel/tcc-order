from app.context import client_ip_context
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ClientIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        client_ip = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.client.host
        client_ip_context.set(client_ip)
        return await call_next(request)
