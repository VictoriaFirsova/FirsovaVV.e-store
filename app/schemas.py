from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductList(ProductBase):
    items: list[Product]


# Схема для элемента заказа
class OrderItem(BaseModel):
    product_id: int
    quantity: int


# Схема для создания заказа (POST /orders)
class OrderCreate(BaseModel):
    items: List[OrderItem]


# Схема для отображения заказа
class Order(BaseModel):
    id: int
    created_at: datetime
    status: str
    items: List[OrderItem]

    class Config:
        orm_mode = True
