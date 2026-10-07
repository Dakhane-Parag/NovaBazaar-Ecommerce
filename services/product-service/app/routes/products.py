import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.schemas.product import ProductListResponse
from app.services import product_service

logger = logging.getLogger("ProductService")

router = APIRouter()

SUPPORTED_SORTS = ["price_asc", "price_desc", "rating_desc"]


@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    sort: str = Query("price_asc"),
):
    if sort not in SUPPORTED_SORTS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid sort value. Supported: {SUPPORTED_SORTS}",
        )

    result = await product_service.list_products(page, limit, category, brand, sort)
    return result


@router.get("/{product_id}")
async def get_product(product_id: str):
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
