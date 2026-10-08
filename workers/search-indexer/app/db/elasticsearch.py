import logging

from elasticsearch import Elasticsearch

from app.core.config import ELASTICSEARCH_INDEX, ELASTICSEARCH_URL

logger = logging.getLogger("SearchIndexer")

es = Elasticsearch([ELASTICSEARCH_URL])


def ensure_index():
    if not es.indices.exists(index=ELASTICSEARCH_INDEX):
        es.indices.create(index=ELASTICSEARCH_INDEX, body={
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "title": {"type": "text", "analyzer": "standard"},
                    "title_suggest": {"type": "completion"},
                    "description": {"type": "text"},
                    "price": {"type": "float"},
                    "category": {"type": "keyword"},
                    "brand": {"type": "keyword"},
                    "images": {"type": "keyword"},
                    "rating": {"type": "float"},
                    "tags": {"type": "keyword"},
                    "attributes": {"type": "object", "enabled": False},
                }
            }
        })
        logger.info(f"Created Elasticsearch index: {ELASTICSEARCH_INDEX}")


def index_product(product):
    doc = {
        "id": product["id"],
        "title": product.get("title", ""),
        "title_suggest": product.get("title", ""),
        "description": product.get("description", ""),
        "price": product.get("price", 0),
        "category": product.get("category", ""),
        "brand": product.get("brand", ""),
        "images": product.get("images", []),
        "rating": product.get("rating", 0),
        "tags": product.get("tags", []),
        "attributes": product.get("attributes", {}),
    }
    es.index(index=ELASTICSEARCH_INDEX, id=product["id"], body=doc)


def update_product(product):
    index_product(product)


def delete_product(product_id):
    es.delete(index=ELASTICSEARCH_INDEX, id=product_id, ignore=[404])
