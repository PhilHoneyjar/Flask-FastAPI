from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    user_id: int
    product_id: int
    order_date: str
    order_status: str


class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: float
