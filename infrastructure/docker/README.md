# Infrastructure

This directory contains Docker infrastructure configurations for local development.

## Services

| Service | Image | Port |
|---------|-------|------|
| PostgreSQL | postgres:16-alpine | 5432 |
| MongoDB | mongo:7 | 27017 |
| Redis | redis:7-alpine | 6379 |
| Kafka | bitnami/kafka:3.7 | 9092 |
| Elasticsearch | elastic/elasticsearch:8.15.0 | 9200 |

## Notes

- All services are defined in the root `docker-compose.yml`
- Persistent volumes are used for all data stores
- Health checks are configured for all services
- All services share the `ecommerce-network` Docker network
