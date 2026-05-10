from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import text
from utils.logger import get_logger
from database import create_tables, engine
from api.v1.requests import router as requests_router

logger = get_logger("request-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Request service starting up...")
    create_tables()
    logger.info("Database tables verified")
    yield
    logger.info("Request service shutting down...")


# FastAPI App
app = FastAPI(lifespan=lifespan, redirect_slashes=False)
app.include_router(requests_router, prefix="/api/v1")


# Custom Exception
class RequestServiceException(Exception):
    """Custom exception for Request Service-level errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Global Exception Handlers
@app.exception_handler(RequestServiceException)
async def request_service_exception_handler(
    request: Request, exc: RequestServiceException
):
    logger.error("Request service Exception occurred: %s", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request service error",
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


# Health Endpoint
@app.get("/health")
def health():
    checks = {}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        logger.error("Health check - database unreachable: %s", e)
        checks["database"] = "unreachable"

    all_ok = all(v == "ok" for v in checks.values())

    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
        },
    )
