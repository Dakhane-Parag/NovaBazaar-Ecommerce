import asyncio
import logging
import os
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s] %(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ProductSeed")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "product_db")

IMG = "https://images.unsplash.com/{}?w=400&h=400&fit=crop"

PRODUCTS = [
    # Electronics
    {"external_product_id": "p-001", "title": "Wireless Noise-Canceling Headphones", "description": "Premium over-ear headphones with active noise cancellation, 30-hour battery life, and crystal-clear audio.", "price": 24999, "category": "electronics", "brand": "Sony", "images": [IMG.format("photo-1505740420928-5e560c06d30e")], "rating": 4.7, "tags": ["headphones", "wireless", "noise-canceling"], "attributes": {"color": "Black", "battery": "30 hours"}},
    {"external_product_id": "p-002", "title": "Smart Watch with AMOLED Display", "description": "Fitness tracker with heart rate monitor, GPS, 7-day battery, and water resistance.", "price": 12999, "category": "electronics", "brand": "Samsung", "images": [IMG.format("photo-1546868871-7041f2a55e12")], "rating": 4.5, "tags": ["smartwatch", "fitness", "wearable"], "attributes": {"color": "Silver", "display": "AMOLED"}},
    {"external_product_id": "p-003", "title": "Instant Camera with Film", "description": "Retro-style instant camera for capturing and printing photos on the go.", "price": 8999, "category": "electronics", "brand": "Fujifilm", "images": [IMG.format("photo-1526170375885-4d8ecf77b99f")], "rating": 4.3, "tags": ["camera", "instant", "retro"], "attributes": {"color": "White", "film_type": "Instax Mini"}},
    {"external_product_id": "p-004", "title": "Portable Bluetooth Speaker", "description": "Waterproof portable speaker with deep bass, 12-hour battery, and rugged design.", "price": 5999, "category": "electronics", "brand": "JBL", "images": [IMG.format("photo-1608043152269-423dbba4e7e1")], "rating": 4.6, "tags": ["speaker", "bluetooth", "portable"], "attributes": {"color": "Blue", "battery": "12 hours"}},
    {"external_product_id": "p-005", "title": "Mechanical Gaming Keyboard", "description": "RGB backlit mechanical keyboard with Cherry MX switches and programmable keys.", "price": 7999, "category": "electronics", "brand": "Logitech", "images": [IMG.format("photo-1587829741301-dc798b83add3")], "rating": 4.4, "tags": ["keyboard", "gaming", "mechanical"], "attributes": {"switch": "Cherry MX Blue", "backlight": "RGB"}},
    # Fashion
    {"external_product_id": "p-006", "title": "Classic White Sneakers", "description": "Minimalist white leather sneakers with cushioned sole for everyday comfort.", "price": 4999, "category": "fashion", "brand": "Nike", "images": [IMG.format("photo-1542291026-7eec264c27ff")], "rating": 4.6, "tags": ["shoes", "sneakers", "casual"], "attributes": {"size": "US 9", "color": "White"}},
    {"external_product_id": "p-007", "title": "Running Shoes Pro", "description": "Lightweight running shoes with responsive cushioning and breathable mesh upper.", "price": 8999, "category": "fashion", "brand": "Adidas", "images": [IMG.format("photo-1595950653106-6c9ebd614d3a")], "rating": 4.5, "tags": ["shoes", "running", "sport"], "attributes": {"size": "US 10", "color": "Black"}},
    {"external_product_id": "p-008", "title": "Polarized Aviator Sunglasses", "description": "Classic aviator sunglasses with polarized lenses and UV protection.", "price": 3499, "category": "fashion", "brand": "Ray-Ban", "images": [IMG.format("photo-1572635196237-14b3f281503f")], "rating": 4.4, "tags": ["sunglasses", "accessories", "uv-protection"], "attributes": {"color": "Gold", "lens": "Polarized"}},
    {"external_product_id": "p-009", "title": "Leather Weekend Bag", "description": "Genuine leather duffel bag with spacious interior and adjustable shoulder strap.", "price": 6999, "category": "fashion", "brand": "Allen Solly", "images": [IMG.format("photo-1548036328-c9fa89d128fa")], "rating": 4.3, "tags": ["bag", "leather", "travel"], "attributes": {"color": "Brown", "material": "Genuine Leather"}},
    {"external_product_id": "p-010", "title": "Minimalist Analog Watch", "description": "Slim analog watch with leather strap and sapphire crystal glass.", "price": 5999, "category": "fashion", "brand": "Fastrack", "images": [IMG.format("photo-1524805444758-089113d48a6d")], "rating": 4.2, "tags": ["watch", "accessories", "minimalist"], "attributes": {"strap": "Leather", "movement": "Quartz"}},
    # Home & Kitchen
    {"external_product_id": "p-011", "title": "Non-Stick Cookware Set", "description": "10-piece non-stick cookware set with even heat distribution and easy cleanup.", "price": 4999, "category": "home-kitchen", "brand": "Prestige", "images": [IMG.format("photo-1556909114-f6e7ad7d3136")], "rating": 4.4, "tags": ["cookware", "non-stick", "kitchen"], "attributes": {"pieces": "10", "material": "Hard Anodized"}},
    {"external_product_id": "p-012", "title": "Cotton Bed Sheet Set", "description": "100% cotton bed sheet set with pillowcases, breathable and soft for all seasons.", "price": 2499, "category": "home-kitchen", "brand": "Wakefit", "images": [IMG.format("photo-1522771739844-6a9f6d5f14af")], "rating": 4.3, "tags": ["bedding", "cotton", "bedroom"], "attributes": {"size": "Queen", "material": "100% Cotton"}},
    {"external_product_id": "p-013", "title": "Ceramic Dinner Plates Set", "description": "Set of 6 ceramic dinner plates, microwave and dishwasher safe.", "price": 1999, "category": "home-kitchen", "brand": "Borosil", "images": [IMG.format("photo-1603199506016-b9a594b593c0")], "rating": 4.1, "tags": ["dinnerware", "ceramic", "kitchen"], "attributes": {"pieces": "6", "material": "Ceramic"}},
    {"external_product_id": "p-014", "title": "Stainless Steel Water Bottle", "description": "Double-wall insulated water bottle, keeps drinks hot/cold for 12 hours.", "price": 999, "category": "home-kitchen", "brand": "Milton", "images": [IMG.format("photo-1602143407151-7111542de6e8")], "rating": 4.5, "tags": ["bottle", "insulated", "kitchen"], "attributes": {"capacity": "1L", "material": "Stainless Steel"}},
    {"external_product_id": "p-015", "title": "Scented Soy Candle Set", "description": "Set of 3 hand-poured soy candles with natural essential oils and 30-hour burn time.", "price": 1299, "category": "home-kitchen", "brand": "IKEA", "images": [IMG.format("photo-1602874801007-bd458bb1b8b6")], "rating": 4.2, "tags": ["candle", "home-decor", "aromatherapy"], "attributes": {"scent": "Lavender", "burn_time": "30 hours"}},
    # Beauty
    {"external_product_id": "p-016", "title": "Luxury Perfume 100ml", "description": "Eau de parfum with notes of jasmine, sandalwood, and vanilla. Long-lasting fragrance.", "price": 4999, "category": "beauty", "brand": "Calvin Klein", "images": [IMG.format("photo-1541643600914-78b084683601")], "rating": 4.6, "tags": ["perfume", "fragrance", "luxury"], "attributes": {"volume": "100ml", "type": "Eau de Parfum"}},
    {"external_product_id": "p-017", "title": "Matte Lipstick Set", "description": "Set of 6 long-wear matte lipsticks in trendy shades, smudge-proof formula.", "price": 1999, "category": "beauty", "brand": "Lakme", "images": [IMG.format("photo-1586495777744-4413f21062fa")], "rating": 4.3, "tags": ["lipstick", "makeup", "matte"], "attributes": {"shades": "6", "finish": "Matte"}},
    {"external_product_id": "p-018", "title": "Vitamin C Face Serum", "description": "Brightening face serum with 15% Vitamin C for glowing, even-toned skin.", "price": 1499, "category": "beauty", "brand": "Minimalist", "images": [IMG.format("photo-1620916566398-39f1143ab7be")], "rating": 4.5, "tags": ["skincare", "serum", "vitamin-c"], "attributes": {"volume": "30ml", "skin_type": "All"}},
    {"external_product_id": "p-019", "title": "Hair Dryer with Ionic Technology", "description": "Professional hair dryer with ionic technology for fast drying and reduced frizz.", "price": 3999, "category": "beauty", "brand": "Philips", "images": [IMG.format("photo-1522338140262-f46f5913618a")], "rating": 4.4, "tags": ["hair-dryer", "styling", "ionic"], "attributes": {"power": "2200W", "technology": "Ionic"}},
    {"external_product_id": "p-020", "title": "Yoga Mat with Carry Strap", "description": "Non-slip yoga mat with alignment lines, 6mm thickness, and carry strap included.", "price": 1499, "category": "fitness", "brand": "Adidas", "images": [IMG.format("photo-1601925260368-ae2f83cf8b7f")], "rating": 4.3, "tags": ["yoga", "fitness", "mat"], "attributes": {"thickness": "6mm", "material": "TPE"}},
]


async def seed():
    logger.info("Product seed started")

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    logger.info(f"Seeding {len(PRODUCTS)} products")

    inserted = 0
    updated = 0

    for item in PRODUCTS:
        product = {
            **item,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        result = await db.products.update_one(
            {"external_product_id": product["external_product_id"]},
            {"$set": product},
            upsert=True,
        )

        if result.upserted_id:
            inserted += 1
        else:
            updated += 1

    logger.info(f"Product seed completed: {inserted} inserted, {updated} updated")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
