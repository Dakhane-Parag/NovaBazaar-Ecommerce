import logging
import os
import threading

from fastapi import FastAPI

from app.consumers import product_events
from app.db import elasticsearch as es

SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
PORT = int(os.getenv("PORT", "8000"))

logging.basicConfig(
    level=logging.INFO,
    format=f"[{SERVICE_NAME}] %(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(SERVICE_NAME)

app = FastAPI(title=SERVICE_NAME)


@app.on_event("startup")
def startup():
    logger.info("Starting application")
    try:
        es.ensure_index()
        logger.info("Elasticsearch connection established")
    except Exception as e:
        logger.error(f"Elasticsearch connection failed: {e}")

    consumer_thread = threading.Thread(target=product_events.start_consumer, daemon=True)
    consumer_thread.start()
    logger.info("Kafka consumer thread started")


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok", "service": SERVICE_NAME}
