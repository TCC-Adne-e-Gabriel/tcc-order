from contextvars import ContextVar

user_id_context: ContextVar[str | None] = ContextVar("user_id_context", default="anonymous")
client_ip_context: ContextVar[str | None] = ContextVar("client_ip_context", default="anonymous")