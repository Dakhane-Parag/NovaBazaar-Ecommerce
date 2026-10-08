import logging
import time

import httpx
from fastapi import APIRouter, Request, Response

from app.core.config import (
    PRODUCT_SERVICE_URL,
    SEARCH_SERVICE_URL,
    REQUEST_TIMEOUT,
)

logger = logging.getLogger("Gateway")

router = APIRouter()

ROUTE_MAP = {
    "/api/products": PRODUCT_SERVICE_URL,
    "/api/search": SEARCH_SERVICE_URL,
}


def get_downstream_url(path: str) -> str | None:
    for prefix, base_url in ROUTE_MAP.items():
        if path.startswith(prefix):
            return base_url
    return None


@router.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request):
    full_path = f"/api/{path}"
    downstream_base = get_downstream_url(full_path)

    if not downstream_base:
        return Response(
            content='{"detail":"Not found"}',
            status_code=404,
            media_type="application/json",
        )

    downstream_path = full_path.replace("/api/", "/", 1)
    downstream_url = f"{downstream_base}{downstream_path}"
    if request.url.query:
        downstream_url += f"?{request.url.query}"

    start = time.time()
    logger.info(f"[Gateway] {request.method} {full_path} -> {downstream_base}")

    try:
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            resp = await client.request(
                method=request.method,
                url=downstream_url,
                headers=headers,
                content=body,
            )

        duration = time.time() - start
        logger.info(
            f"[Gateway] {request.method} {full_path} -> {resp.status_code} ({duration:.2f}s)"
        )

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
            media_type=resp.headers.get("content-type", "application/json"),
        )

    except httpx.TimeoutException:
        duration = time.time() - start
        logger.error(f"[Gateway] {request.method} {full_path} -> TIMEOUT ({duration:.2f}s)")
        return Response(
            content='{"detail":"Service timeout. Please try again."}',
            status_code=504,
            media_type="application/json",
        )
    except httpx.ConnectError:
        duration = time.time() - start
        logger.error(f"[Gateway] {request.method} {full_path} -> SERVICE UNAVAILABLE ({duration:.2f}s)")
        return Response(
            content='{"detail":"Service unavailable. Please try again later."}',
            status_code=502,
            media_type="application/json",
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(f"[Gateway] {request.method} {full_path} -> ERROR: {e} ({duration:.2f}s)")
        return Response(
            content='{"detail":"Internal server error"}',
            status_code=500,
            media_type="application/json",
        )
