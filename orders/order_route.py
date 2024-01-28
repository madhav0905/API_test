from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pymongo import MongoClient, DESCENDING
from pydantic import BaseModel,PositiveInt, ValidationError
from models.products import ProductResponseItem, ProductsResponse,Product
from models.orders import Order, OrderItem, UserAddress
import logging
logging.basicConfig(level=logging.DEBUG)
from db import orders_collection
app = APIRouter()


# API to create a new order
@app.post("/orders/", response_model=dict)
async def create_order(order: Order):
    if not order.items:
        return JSONResponse(content={"detail": "Order items is empty"}, status_code=400)
    for item in order.items:
        try:
            product = products_collection.find_one({"_id": item.productId})
            if not product or item.boughtQuantity <= 0:
                raise ValidationError([{"loc": ["body"], "msg": "Invalid product or quantity", "type": "value_error"}])
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e)) 
    order_data = {
        "items": [
            {
                "productId": item.productId,
                "boughtQuantity": item.boughtQuantity,
                "totalAmount": item.totalAmount,
            }
            for item in order.items
        ],
        "userAddress": {
            "city": order.userAddress.city,
            "country": order.userAddress.country,
            "zipCode": order.userAddress.zipCode,
        },
    }

    result = orders_collection.insert_one(order_data)
    order_id = str(result.inserted_id)

    return {"orderId": order_id}