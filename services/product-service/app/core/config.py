import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "product_db")
PRODUCT_SEED_API_URL = os.getenv("PRODUCT_SEED_API_URL", "https://fakestoreapi.com/products")
