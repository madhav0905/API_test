from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Model for Order
class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int
    totalAmount: float

class UserAddress(BaseModel):
    city: str
    country: str
    zipCode: str

class Order(BaseModel):
    items: List[OrderItem]
    userAddress: UserAddress
    createdOn: datetime = datetime.utcnow()
