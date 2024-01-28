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

    pipeline = [
        {
            "$lookup": {
                "from": "products",    # Name of the products collection
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "product_info"
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$unwind": "$product_info"
        },
        {
            "$project": {
                "productId": "$items.productId",
                "boughtQuantity": "$items.boughtQuantity",
                "productName": "$product_info.name",  # Include other fields as needed
                "productPrice": "$product_info.price"
            }
        }
    ]

    totalAmount = 0.0
    for item in order.items:
        try:
            product_info = list(products_collection.aggregate(pipeline, allowDiskUse=True))[0]
            if not product_info or item.boughtQuantity <= 0:
                raise ValidationError([{"loc": ["body"], "msg": "Invalid product or quantity", "type": "value_error"}])
            else:
                totalAmount += item.boughtQuantity * product_info["productPrice"]
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    order_data = {
        "items": [
            {
                "productId": item["productId"],
                "boughtQuantity": item["boughtQuantity"],
                "productName": item["productName"],
                "productPrice": item["productPrice"]
            }
            for item in order.items
        ],
        "userAddress": {
            "city": order.userAddress.city,
            "country": order.userAddress.country,
            "zipCode": order.userAddress.zipCode,
        },
        "totalAmount": totalAmount
    }

    result = orders_collection.insert_one(order_data)
    order_id = str(result.inserted_id)

    return {"orderId": order_id}