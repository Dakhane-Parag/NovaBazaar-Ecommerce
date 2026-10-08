import logging

from elasticsearch import Elasticsearch

from app.core.config import ELASTICSEARCH_INDEX, ELASTICSEARCH_URL

logger = logging.getLogger("SearchService")

es = Elasticsearch([ELASTICSEARCH_URL])

INDEX_MAPPING = {
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
}


def ensure_index():
    if not es.indices.exists(index=ELASTICSEARCH_INDEX):
        es.indices.create(index=ELASTICSEARCH_INDEX, body=INDEX_MAPPING)
        logger.info(f"Created Elasticsearch index: {ELASTICSEARCH_INDEX}")
    else:
        logger.info(f"Elasticsearch index already exists: {ELASTICSEARCH_INDEX}")


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


def search_products(query, filters, sort, page, limit):
    must = []
    filter_clauses = []

    if query:
        must.append({
            "multi_match": {
                "query": query,
                "fields": ["title^3", "description", "brand^2", "tags^2"],
                "fuzziness": "AUTO",
            }
        })

    if filters.get("category"):
        filter_clauses.append({"term": {"category": filters["category"]}})
    if filters.get("brand"):
        filter_clauses.append({"term": {"brand": filters["brand"]}})
    if filters.get("minPrice") is not None or filters.get("maxPrice") is not None:
        range_clause = {"range": {"price": {}}}
        if filters.get("minPrice") is not None:
            range_clause["range"]["price"]["gte"] = filters["minPrice"]
        if filters.get("maxPrice") is not None:
            range_clause["range"]["price"]["lte"] = filters["maxPrice"]
        filter_clauses.append(range_clause)
    if filters.get("minRating") is not None:
        filter_clauses.append({"range": {"rating": {"gte": filters["minRating"]}}})

    sort_clause = []
    if sort == "price_asc":
        sort_clause = [{"price": "asc"}]
    elif sort == "price_desc":
        sort_clause = [{"price": "desc"}]
    elif sort == "rating_desc":
        sort_clause = [{"rating": "desc"}]

    body = {
        "query": {
            "bool": {
                "must": must if must else [{"match_all": {}}],
                "filter": filter_clauses,
            }
        },
        "from": (page - 1) * limit,
        "size": limit,
    }
    if sort_clause:
        body["sort"] = sort_clause

    response = es.search(index=ELASTICSEARCH_INDEX, body=body)
    hits = response["hits"]["hits"]
    total = response["hits"]["total"]["value"]

    items = []
    for hit in hits:
        item = hit["_source"]
        item["id"] = hit["_id"]
        items.append(item)

    return items, total


def get_suggestions(prefix):
    body = {
        "query": {
            "match_phrase_prefix": {
                "title": {
                    "query": prefix,
                    "max_expansions": 5,
                }
            }
        },
        "size": 5,
    }
    response = es.search(index=ELASTICSEARCH_INDEX, body=body)
    hits = response["hits"]["hits"]
    seen = set()
    suggestions = []
    for hit in hits:
        title = hit["_source"].get("title", "")
        if title and title not in seen:
            seen.add(title)
            suggestions.append(title)
    return suggestions
