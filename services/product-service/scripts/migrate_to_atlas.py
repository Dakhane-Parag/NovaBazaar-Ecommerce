import asyncio
import logging
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logger = logging.getLogger("Migration")

LOCAL_URI = "mongodb://localhost:27017"
ATLAS_URI = os.getenv("MONGO_URI", "").strip('"').strip("'")
DB_NAME = os.getenv("MONGO_DB_NAME", "product_db")


async def migrate():
    if not ATLAS_URI or "localhost" in ATLAS_URI:
        logger.error("MONGO_URI in .env is not set to Atlas. Please update .env with your Atlas connection string.")
        return

    logger.info("Connecting to local MongoDB...")
    local_client = MongoClient(LOCAL_URI)
    local_db = local_client[DB_NAME]
    local_count = local_db.products.count_documents({})
    logger.info(f"Local products found: {local_count}")

    if local_count == 0:
        logger.info("No local products to migrate. Running seed on Atlas instead...")
        local_client.close()
        return

    logger.info("Connecting to MongoDB Atlas...")
    atlas_client = AsyncIOMotorClient(ATLAS_URI)
    atlas_db = atlas_client[DB_NAME]

    products = list(local_db.products.find({}))
    logger.info(f"Migrating {len(products)} products to Atlas...")

    for product in products:
        product.pop("_id", None)
        await atlas_db.products.update_one(
            {"external_product_id": product["external_product_id"]},
            {"$set": product},
            upsert=True,
        )

    atlas_count = await atlas_db.products.count_documents({})
    logger.info(f"Migration complete! Atlas now has {atlas_count} products.")

    local_client.close()
    atlas_client.close()


if __name__ == "__main__":
    asyncio.run(migrate())
