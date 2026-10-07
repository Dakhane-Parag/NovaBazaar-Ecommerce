from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "product-service"


@pytest.mark.asyncio
async def test_list_products(client):
    mock_products = [
        {
            "_id": "507f1f77bcf86cd799439011",
            "title": "iPhone 15",
            "price": 69999,
            "category": "smartphones",
            "brand": "Apple",
            "images": ["https://example.com/iphone.jpg"],
            "rating": 4.8,
        }
    ]

    with patch(
        "app.repositories.product_repository.get_products",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = (mock_products, 1)

        response = await client.get("/products?page=1&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["limit"] == 20
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "iPhone 15"
        assert data["items"][0]["id"] == "507f1f77bcf86cd799439011"


@pytest.mark.asyncio
async def test_list_products_pagination(client):
    mock_products = [
        {"_id": f"507f1f77bcf86cd79943901{i}", "title": f"Product {i}", "price": 100, "category": "test"}
        for i in range(1, 4)
    ]

    with patch(
        "app.repositories.product_repository.get_products",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = (mock_products, 50)

        response = await client.get("/products?page=2&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        assert data["total"] == 50


@pytest.mark.asyncio
async def test_list_products_category_filter(client):
    with patch(
        "app.repositories.product_repository.get_products",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = ([], 0)

        response = await client.get("/products?category=smartphones")
        assert response.status_code == 200
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][2] == {"category": "smartphones"}


@pytest.mark.asyncio
async def test_list_products_brand_filter(client):
    with patch(
        "app.repositories.product_repository.get_products",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = ([], 0)

        response = await client.get("/products?brand=Apple")
        assert response.status_code == 200
        call_args = mock_get.call_args
        assert call_args[0][2] == {"brand": "Apple"}


@pytest.mark.asyncio
async def test_list_products_sort_price_desc(client):
    with patch(
        "app.repositories.product_repository.get_products",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = ([], 0)

        response = await client.get("/products?sort=price_desc")
        assert response.status_code == 200
        call_args = mock_get.call_args
        assert ("price", -1) in call_args[0][3]


@pytest.mark.asyncio
async def test_list_products_invalid_sort(client):
    response = await client.get("/products?sort=invalid_sort")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_products_invalid_pagination(client):
    response = await client.get("/products?page=0")
    assert response.status_code == 422

    response = await client.get("/products?limit=0")
    assert response.status_code == 422

    response = await client.get("/products?limit=200")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_product_by_id_success(client):
    mock_product = {
        "_id": "507f1f77bcf86cd799439011",
        "title": "iPhone 15",
        "price": 69999,
        "category": "smartphones",
        "brand": "Apple",
        "images": ["https://example.com/iphone.jpg"],
        "rating": 4.8,
    }

    with patch(
        "app.repositories.product_repository.get_product_by_id",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = mock_product

        response = await client.get("/products/507f1f77bcf86cd799439011")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "507f1f77bcf86cd799439011"
        assert data["title"] == "iPhone 15"


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(client):
    with patch(
        "app.repositories.product_repository.get_product_by_id",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = None

        response = await client.get("/products/507f1f77bcf86cd799439099")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_product_by_id_invalid_id(client):
    response = await client.get("/products/invalid-id")
    assert response.status_code == 404
