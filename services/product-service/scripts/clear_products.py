import asyncio
import logging
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logger = logging.getLogger("ClearProducts")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "product_db")


async def clear():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    result = await db.products.delete_many({})
    logger.info(f"Cleared {result.deleted_count} products from MongoDB")
    client.close()


if __name__ == "__main__":
    asyncio.run(clear())
