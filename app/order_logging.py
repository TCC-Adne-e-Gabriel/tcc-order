import logging
import sys
import logging
from app.context import user_id_context, client_ip_context

AUDIT_LEVEL_NUM = 25
logging.addLevelName(AUDIT_LEVEL_NUM, "AUDIT")

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level

class ContextLoggerAdapter(logging.LoggerAdapter):      
    def audit(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if self.isEnabledFor(AUDIT_LEVEL_NUM):
            self._log(AUDIT_LEVEL_NUM, msg, args, **kwargs)
            
    def process(self, msg, kwargs):
        user_id = user_id_context.get()
        client_ip = client_ip_context.get()
        extra = kwargs.get("extra", {})
        extra["user_id"] = user_id
        extra["client_ip"] = client_ip
        kwargs["extra"] = extra
        return msg, kwargs
    

formatter = logging.Formatter(
    fmt="%(levelname)s: %(asctime)s - USUARIO %(user_id)s from %(client_ip)s - %(message)s"
)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.addFilter(MaxLevelFilter(logging.WARNING))
stdout_handler.setLevel(logging.INFO)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
stderr_handler.setLevel(logging.WARN)


logger = logging.getLogger("app")
logger.handlers = [stdout_handler, stderr_handler]
logger.setLevel(logging.INFO)
logger.propagate = False 

logger = ContextLoggerAdapter(logger, {})
