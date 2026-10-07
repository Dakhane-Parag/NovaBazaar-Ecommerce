import logging
from typing import Any, Dict, List, Optional, Tuple

from app.repositories import product_repository

logger = logging.getLogger("ProductService")

SORT_MAP: Dict[str, List[Tuple[str, int]]] = {
    "price_asc": [("price", 1)],
    "price_desc": [("price", -1)],
    "rating_desc": [("rating", -1)],
}


async def list_products(
    page: int,
    limit: int,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    sort: str = "price_asc",
) -> Dict[str, Any]:
    skip = (page - 1) * limit

    filters: Dict[str, Any] = {}
    if category:
        filters["category"] = category
    if brand:
        filters["brand"] = brand

    sort_clause = SORT_MAP.get(sort, SORT_MAP["price_asc"])

    logger.info(f"Fetching products: page={page}, limit={limit}, filters={filters}, sort={sort}")
    products, total = await product_repository.get_products(skip, limit, filters, sort_clause)

    return {
        "items": [_format_product(p) for p in products],
        "page": page,
        "limit": limit,
        "total": total,
    }


async def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    logger.info(f"Fetching product: {product_id}")
    product = await product_repository.get_product_by_id(product_id)
    if product:
        logger.info(f"Product retrieved: {product_id}")
        return _format_product(product)
    logger.info(f"Product not found: {product_id}")
    return None


def _format_product(product: Dict[str, Any]) -> Dict[str, Any]:
    product["id"] = str(product.pop("_id"))
    return product
