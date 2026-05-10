from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from utils.logger import get_logger
from api.v1.requests import router as request_router
import os
import httpx


logger = get_logger("gateway")


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gateway service starting up...")
    yield
    logger.info("Gateway service shutting down...")


# FastAPI App
app = FastAPI(lifespan=lifespan, redirect_slashes=False)
app.include_router(request_router, prefix="/api/v1")


# Custom Exception
class GatewayException(Exception):
    """Custom exception for gateway-level errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Global Exception Handlers
@app.exception_handler(GatewayException)
async def gateway_exception_handler(request: Request, exc: GatewayException):
    logger.error("GatewayException occurred: %s", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Gateway error",
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

    services = {
        "request-service": "http://request-service:8000/health",
        "location-service": "http://location-service:8000/health",
    }

    for name, url in services.items():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=3.0)
            checks[name] = "ok" if response.status_code == 200 else "degraded"
        except Exception as e:
            logger.error("Health check — %s unreachable: %s", name, e)
            checks[name] = "unreachable"

    all_ok = all(v == "ok" for v in checks.values())

    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
        },
    )
