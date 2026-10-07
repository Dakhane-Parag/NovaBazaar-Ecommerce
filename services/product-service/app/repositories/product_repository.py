import logging
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId

from app.db.mongodb import db

logger = logging.getLogger("ProductService")


async def get_products(
    skip: int,
    limit: int,
    filters: Dict[str, Any],
    sort: List[Tuple[str, int]],
) -> Tuple[List[Dict[str, Any]], int]:
    cursor = db.products.find(filters).sort(sort).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    total = await db.products.count_documents(filters)
    return products, total


async def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    try:
        obj_id = ObjectId(product_id)
    except Exception:
        logger.warning(f"Invalid product ID format: {product_id}")
        return None
    product = await db.products.find_one({"_id": obj_id})
    return product


async def find_by_external_id(external_id: str) -> Optional[Dict[str, Any]]:
    return await db.products.find_one({"external_product_id": external_id})


async def upsert_product(product: Dict[str, Any]) -> None:
    await db.products.update_one(
        {"external_product_id": product["external_product_id"]},
        {"$set": product},
        upsert=True,
    )
