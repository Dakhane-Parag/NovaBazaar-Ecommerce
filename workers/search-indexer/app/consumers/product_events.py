import json
import logging

from confluent_kafka import Consumer

from app.core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, KAFKA_PRODUCT_TOPIC
from app.db import elasticsearch as es

logger = logging.getLogger("SearchIndexer")


def start_consumer():
    consumer = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": KAFKA_GROUP_ID,
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe([KAFKA_PRODUCT_TOPIC])

    logger.info(f"Kafka consumer started, subscribed to: {KAFKA_PRODUCT_TOPIC}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            try:
                event = json.loads(msg.value().decode("utf-8"))
                handle_event(event)
            except Exception as e:
                logger.error(f"Failed to process event: {e}")
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        consumer.close()


def handle_event(event):
    event_id = event.get("event_id", "")
    event_type = event.get("event_type", "")
    payload = event.get("payload", {})

    logger.info(f"Processing event: {event_type} (id: {event_id})")

    if event_type == "ProductCreated":
        es.index_product(payload)
        logger.info(f"Indexed product: {payload.get('id')}")
    elif event_type == "ProductUpdated":
        es.update_product(payload)
        logger.info(f"Updated product: {payload.get('id')}")
    elif event_type == "ProductDeleted":
        es.delete_product(payload.get("id"))
        logger.info(f"Deleted product: {payload.get('id')}")
    else:
        logger.warning(f"Unknown event type: {event_type}")
