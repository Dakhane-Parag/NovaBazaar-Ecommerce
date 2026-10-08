import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.db import elasticsearch as es

logger = logging.getLogger("SearchService")

router = APIRouter()

SUPPORTED_SORTS = ["price_asc", "price_desc", "rating_desc"]


@router.get("/search")
async def search(
    q: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    minRating: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("price_asc"),
):
    if sort not in SUPPORTED_SORTS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid sort value. Supported: {SUPPORTED_SORTS}",
        )

    filters = {
        "category": category,
        "brand": brand,
        "minPrice": minPrice,
        "maxPrice": maxPrice,
        "minRating": minRating,
    }

    logger.info(f"Search: q={q}, filters={filters}, sort={sort}, page={page}")
    items, total = es.search_products(q, filters, sort, page, limit)

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
    }


@router.get("/search/suggestions")
async def suggestions(q: str = Query(..., min_length=1)):
    logger.info(f"Suggestions: q={q}")
    results = es.get_suggestions(q)
    return {"suggestions": results}
