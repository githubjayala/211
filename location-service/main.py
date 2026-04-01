from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from logger import get_logger


logger = get_logger("location-service")


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Location service starting up...")
    yield
    logger.info("Location service shutting down...")


# FastAPI App
app = FastAPI(lifespan=lifespan)


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
    try:
        logger.info("Health check invoked")
        return {"status": "ok"}
    except Exception as exc:
        logger.error("Health check failure: %s", exc)
        raise LocationServiceException("Health check failed", status_code=500)
