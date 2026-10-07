# NovaBazaar

A production-style e-commerce platform built with microservices architecture.

## Project Overview

This project demonstrates a scalable e-commerce platform using:
- Microservice architecture with clear service boundaries
- REST for synchronous communication
- Kafka for asynchronous event-driven communication
- Multiple data stores (PostgreSQL, MongoDB, Redis, Elasticsearch)
- Google OAuth for authentication
- Razorpay for payments

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| Databases | PostgreSQL, MongoDB |
| Cache | Redis |
| Search | Elasticsearch |
| Messaging | Kafka |
| Containerization | Docker, Docker Compose |

## Repository Structure

```
.
├── frontend/                  # React + Vite + Tailwind CSS
├── services/                  # Backend microservices
│   ├── api-gateway/
│   ├── user-service/
│   ├── product-service/
│   ├── search-service/
│   ├── cart-service/
│   ├── inventory-service/
│   ├── order-service/
│   ├── payment-service/
│   └── notification-service/
├── workers/
│   └── search-indexer/        # Kafka consumer for search indexing
├── infrastructure/
│   └── docker/                # Docker infrastructure configs
├── docker-compose.yml         # Local development infrastructure
├── .env.example               # Environment variable template
└── README.md
```

## Local Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Node.js 20+

### Quick Start

1. **Clone the repository**

2. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```

3. **Start infrastructure with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Start a backend service (example: product-service)**
   ```bash
   cd services/product-service
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
   ```

5. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Docker Compose Commands

```bash
# Start all infrastructure services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## Service Ports

| Service | Port |
|---------|------|
| API Gateway | 8100 |
| User Service | 8101 |
| Product Service | 8502 |
| Search Service | 8103 |
| Cart Service | 8104 |
| Inventory Service | 8105 |
| Order Service | 8106 |
| Payment Service | 8107 |
| Notification Service | 8108 |
| Frontend | 5173 |

### Infrastructure Ports

| Service | Port |
|---------|------|
| PostgreSQL | 5432 |
| MongoDB | 27017 |
| Redis | 6379 |
| Kafka | 9092 |
| Elasticsearch | 9200 |

## Health Check Endpoints

Every backend service exposes a health check endpoint:

```
GET /health
```

Response:
```json
{
  "status": "ok",
  "service": "product-service"
}
```

## Architecture Overview

```
                    ┌─────────────┐
                    │   Frontend  │
                    │  (React)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ API Gateway │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │  User   │      │  Product  │     │  Search   │
   │ Service │      │  Service  │     │  Service  │
   └────┬────┘      └─────┬─────┘     └─────┬─────┘
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │PostgreSQL│      │  MongoDB  │     │Elasticsearch
   └─────────┘      └───────────┘     └───────────┘

        ┌──────────────────┬──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │  Cart   │      │ Inventory │     │  Order    │
   │ Service │      │  Service  │     │  Service  │
   └────┬────┘      └─────┬─────┘     └─────┬─────┘
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │  Redis  │      │PostgreSQL │     │PostgreSQL │
   └─────────┘      └───────────┘     └───────────┘

   ┌─────────┐      ┌───────────┐
   │ Payment │      │Notification│
   │ Service │      │  Service   │
   └────┬────┘      └─────┬─────┘
        │                  │
   ┌────▼────┐      ┌─────▼─────┐
   │PostgreSQL│      │PostgreSQL │
   └─────────┘      └───────────┘

        ┌──────────────────────────┐
        │         Kafka            │
        │  (Async Event Transport) │
        └──────────────────────────┘
```

## Data Store Responsibilities

| Data Store | Owns |
|-----------|------|
| MongoDB | Products (source of truth) |
| PostgreSQL | Users, Inventory, Orders, Payments, Notifications |
| Redis | Carts, Reservations, Sessions, Caching |
| Elasticsearch | Search index (not source of truth) |
| Kafka | Asynchronous event transport |

## Current Implementation Status

**Currently implemented: Stair 1 — Product Catalog**

- [x] Monorepo structure
- [x] FastAPI service skeletons with /health endpoints
- [x] React + Vite + Tailwind CSS frontend
- [x] Docker Compose for local infrastructure
- [x] Environment variable configuration
- [x] Basic logging conventions
- [x] Product Service with MongoDB
- [x] Product seeding from external API
- [x] Product listing with pagination, filtering, sorting
- [x] Product detail endpoint

### Planned Stairs

- [ ] Stair 2 — Search
- [ ] Stair 3 — Authentication (Google OAuth)
- [ ] Stair 4 — Cart
- [ ] Stair 5 — Inventory
- [ ] Stair 6 — Orders
- [ ] Stair 7 — Payments (Razorpay)
- [ ] Stair 8 — Notifications

## License

MIT
