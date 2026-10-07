import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
PORT = int(os.getenv("PORT", "8000"))

logging.basicConfig(
    level=logging.INFO,
    format=f"[{SERVICE_NAME}] %(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(SERVICE_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    yield
    logger.info("Shutting down application")


app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok", "service": SERVICE_NAME}
