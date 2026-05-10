from api.v1 import locations
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from utils.logger import get_logger
from api.v1.locations import router as location_router
import httpx


logger = get_logger("location-service")


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Location service starting up...")
    yield
    logger.info("Location service shutting down...")


# FastAPI App
app = FastAPI(lifespan=lifespan, redirect_slashes=False)
app.include_router(location_router, prefix="/api/v1")


# Custom Exception
class LocationServiceException(Exception):
    """Custom exception for Location Service-level errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Global Exception Handlers
@app.exception_handler(LocationServiceException)
async def location_service_exception_handler(
    request: Request, exc: LocationServiceException
):
    logger.error("Location service Exception occurred: %s", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "location service error",
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
async def health():
    checks = {}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://nominatim.openstreetmap.org/status",
                headers={"User-Agent": "211-civic-platform/1.0"},
                timeout=5.0,
            )
        checks["nominatim"] = "ok" if response.status_code == 200 else "unreachable"
    except Exception as e:
        logger.error("Health check — Nominatim unreachable: %s", e)
        checks["nominatim"] = "unreachable"

    all_ok = all(v == "ok" for v in checks.values())

    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
        },
    )
