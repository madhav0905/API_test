import logging
from pymongo import MongoClient, DESCENDING
logging.basicConfig(level=logging.DEBUG)
logging.debug("Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017/")
logging.debug("Connected to MongoDB.")
logging.debug(f"MongoDB Host: {client.HOST}")
logging.debug(f"MongoDB Port: {client.PORT}")
logging.debug("Available databases:")
logging.debug(client.list_database_names())
db = client["ecommerce"]
products_collection = db["products"]
orders_collection = db["orders"]
