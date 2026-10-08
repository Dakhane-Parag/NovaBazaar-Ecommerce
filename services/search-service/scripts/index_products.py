import asyncio
import logging
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logger = logging.getLogger("IndexProducts")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "product_db")


async def index_all():
    from app.db import elasticsearch as es

    logger.info("Starting bulk index from MongoDB to Elasticsearch")

    es.ensure_index()

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    cursor = db.products.find({})
    count = 0

    async for product in cursor:
        product["id"] = str(product.pop("_id"))
        es.index_product(product)
        count += 1
        if count % 10 == 0:
            logger.info(f"Indexed {count} products...")

    logger.info(f"Bulk index complete: {count} products indexed")
    client.close()


if __name__ == "__main__":
    asyncio.run(index_all())
