from pydantic import BaseModel
from typing import List, Optional
class Product(BaseModel):
    name: str
    price: float
    quantity: int

class ProductResponseItem(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

#  Pydantic model for the response
class ProductsResponse(BaseModel):
    data: List[ProductResponseItem]
    page: dict
