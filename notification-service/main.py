from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from utils.logger import get_logger
from utils.middleware import TracingMiddleware
import asyncio
from consumer import start_consumer

logger = get_logger("notifications-service")


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Notification service starting up...")
    asyncio.create_task(start_consumer())
    yield
    logger.info("Notification service shutting down...")


# FastAPI App
app = FastAPI(lifespan=lifespan)
app.add_middleware(TracingMiddleware)


# Custom Exception
class NotificationServiceException(Exception):
    """Custom exception for Notification Service-level errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Global Exception Handlers
@app.exception_handler(NotificationServiceException)
async def notification_service_exception_handler(
    request: Request, exc: NotificationServiceException
):
    logger.error("Notification service Exception occurred: %s", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Notification service error",
            "request_id": request.headers.get("X-Request-ID"),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": request.headers.get("X-Request-ID"),
        },
    )


@app.get("/health")
async def health():
    import os
    import aio_pika

    checks = {}

    try:
        conn = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
        await conn.close()
        checks["rabbitmq"] = "ok"
    except Exception as e:
        logger.error("Health check — RabbitMQ unreachable: %s", e)
        checks["rabbitmq"] = "unreachable"

    all_ok = all(v == "ok" for v in checks.values())

    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
        },
    )
