import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGO_DB_NAME, MONGO_URI

logger = logging.getLogger("ProductService")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

logger.info("MongoDB client initialized")
