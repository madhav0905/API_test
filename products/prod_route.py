from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pymongo import MongoClient, DESCENDING
from pydantic import BaseModel,PositiveInt, ValidationError
from models.products import ProductResponseItem, ProductsResponse,Product
from models.orders import Order, OrderItem, UserAddress
import logging
logging.basicConfig(level=logging.DEBUG)
from db import products_collection
app = APIRouter()
# API to list all available products
@app.get("/products/", response_model=dict)
async def list_products(
    limit: int = Query(10, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    min_price: Optional[float] = Query(None, description="Minimum product price"),
    max_price: Optional[float] = Query(None, description="Maximum product price"),
):
    query_params = {}
    if min_price is not None:
        query_params["price"] = {"$gte": min_price}
    if max_price is not None:
        query_params["price"] = {"$lte": max_price}

    products = list(
        products_collection.find(query_params)
        .skip(offset)
        .limit(limit)
        .sort([("_id", DESCENDING)])
    )

    total_records = products_collection.count_documents(query_params)

    response_data = {
        "data": [
            {
                "id": str(product["_id"]),
                "name": product["name"],
                "price": product["price"],
                "quantity": product["quantity"],
            }
            for product in products
        ],
        "page": {
            "limit": limit,
            "nextOffset": offset + limit if offset + limit < total_records else None,
            "prevOffset": offset - limit if offset - limit >= 0 else None,
            "total": total_records,
        },
    }

    return response_data

@app.post("/products/", response_model=dict)
async def create_product(product: Product):
    result = products_collection.insert_one(product.dict())
    # Return the created product as the response
    logging.debug(result)
    product_id = str(result.inserted_id)

    return {"orderId": product_id}
