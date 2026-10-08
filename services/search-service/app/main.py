import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import elasticsearch as es
from app.routes import search

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
    try:
        es.ensure_index()
        logger.info("Elasticsearch connection established")
    except Exception as e:
        logger.error(f"Elasticsearch connection failed: {e}")
    yield
    logger.info("Shutting down application")


app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, tags=["search"])


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok", "service": SERVICE_NAME}
