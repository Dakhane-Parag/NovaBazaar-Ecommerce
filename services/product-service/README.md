# Product Service

Manages the product catalog for NovaBazaar.

## Purpose

The Product Service owns the product catalog. It reads products from MongoDB, which is the source of truth. An external product API is used only for initial seeding — never during normal requests.

## MongoDB

- **Database:** `product_db`
- **Collection:** `products`

### Indexes

| Index | Purpose |
|-------|---------|
| `external_product_id` (unique) | Idempotent seeding — prevents duplicate imports |
| `category` | Fast category filtering |
| `brand` | Fast brand filtering |
| `price` | Fast price sorting |
| `rating` | Fast rating sorting |

## Product Schema

```json
{
    "_id": "ObjectId",
    "external_product_id": "string (from seed API)",
    "title": "string",
    "description": "string",
    "price": "float (>= 0)",
    "category": "string",
    "brand": "string",
    "images": ["string"],
    "rating": "float (0-5)",
    "tags": ["string"],
    "attributes": {},
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## API Endpoints

### GET /products

List products with pagination, filtering, and sorting.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number (>= 1) |
| `limit` | int | 20 | Items per page (1-100) |
| `category` | string | — | Filter by category |
| `brand` | string | — | Filter by brand |
| `sort` | string | price_asc | Sort order: `price_asc`, `price_desc`, `rating_desc` |

**Response:**
```json
{
    "items": [
        {
            "id": "507f1f77bcf86cd799439011",
            "title": "iPhone 15",
            "price": 69999,
            "category": "smartphones",
            "brand": "Apple",
            "images": ["https://..."],
            "rating": 4.8
        }
    ],
    "page": 1,
    "limit": 20,
    "total": 100
}
```

### GET /products/{product_id}

Get a single product by ID.

**Response:** Product object (same format as above)

**Errors:**
- `404` — Product not found
- `400` — Invalid product ID format

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string (Atlas or local) |
| `MONGO_DB_NAME` | `product_db` | Database name |
| `PRODUCT_SEED_API_URL` | `https://dummyjson.com/products` | External API for seeding |
| `SERVICE_NAME` | `product-service` | Service name for logging |
| `PORT` | `8000` | Server port |

### MongoDB Atlas Setup

1. Create a free cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create a database user
3. Add your IP to the Network Access list (or allow all: `0.0.0.0/0`)
4. Get your connection string: `mongodb+srv://<user>:<password>@<cluster>.mongodb.net`
5. Set `MONGO_URI` to that connection string

Example:
```
MONGO_URI=mongodb+srv://admin:password123@cluster0.abc123.mongodb.net
```

## Seeding

To seed products from the external API:

```bash
cd services/product-service
python -m scripts.seed_products.py
```

The seed script is idempotent — running it multiple times will not create duplicate products. It uses `external_product_id` as a unique key.

## Running Locally

```bash
cd services/product-service
pip install -r requirements.txt
export SERVICE_NAME=product-service
export PORT=8102
export MONGO_URI=mongodb://localhost:27017
python -m uvicorn app.main:app --host 0.0.0.0 --port 8102 --reload
```

## Running with Docker

```bash
docker compose up -d product-service
```

The service connects to MongoDB using the Docker service hostname `mongodb`.

## Testing

```bash
cd services/product-service
pip install -r requirements.txt
pytest tests/ -v
```

## API Documentation

FastAPI auto-generates Swagger docs at `/docs` and OpenAPI spec at `/openapi.json`.
