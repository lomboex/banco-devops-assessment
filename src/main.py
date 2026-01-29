from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import structlog
from contextlib import asynccontextmanager

from core.config import settings
from utils.logger import configure_logger
from routers import devops

configure_logger()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

Instrumentator().instrument(app).expose(app)

app.include_router(devops.router)


@app.get("/healthz", status_code=200)
async def health_check():
    return {"status": "ok"}


@app.get("/readyz", status_code=200)
async def readiness_check():
    return {"status": "ready"}


@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    return JSONResponse(
        status_code=405,
        content="ERROR"
    )
