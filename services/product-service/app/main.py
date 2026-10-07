import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongodb import client, db
from app.routes import products

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
        await db.products.create_index("external_product_id", unique=True)
        await db.products.create_index("category")
        await db.products.create_index("brand")
        await db.products.create_index("price")
        await db.products.create_index("rating")
        logger.info("MongoDB connection established")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
    yield
    client.close()
    logger.info("Shutting down application")


app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products", tags=["products"])


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok", "service": SERVICE_NAME}
