# Search Indexer

Kafka consumer that indexes product events into Elasticsearch.

## Responsibilities (future)

- Consume product events from Kafka (product-events topic)
- Index/update/delete products in Elasticsearch
- Idempotent event processing

## Data Flow

```
Product Service → Kafka (product-events) → Search Indexer → Elasticsearch
```

## Status

Stair 0: Skeleton only. Indexing logic will be implemented in later stairs.
