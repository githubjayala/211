import logging
import sys
from datetime import datetime


class StructuredFormatter(logging.Formatter):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name

    def format(self, record):
        timestamp = datetime.utcnow().isoformat()
        level = record.levelname
        message = record.getMessage()
        return f"{timestamp} | {level} | {self.service_name} | {message}"


def get_logger(service_name: str) -> logging.Logger:
    """
    Returns a structured,
    PII-safe logger configured for the given service.
    """
    logger = logging.getLogger(service_name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter(service_name))
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
