# Inventory Service

Manages product inventory and stock reservations.

## Responsibilities (future)

- Stock tracking (total, available, reserved, sold)
- Atomic inventory reservations
- Reservation expiration (5-minute TTL)
- Stock release on expiration

## Data Store

- PostgreSQL (inventory_db) — durable inventory records
- Redis — fast atomic reservation layer

## Status

Stair 0: Skeleton only. Inventory functionality will be implemented in later stairs.
