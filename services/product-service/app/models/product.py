from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    external_product_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    category: str
    brand: Optional[str] = None
    images: List[str] = []
    rating: Optional[float] = Field(None, ge=0, le=5)
    tags: List[str] = []
    attributes: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
