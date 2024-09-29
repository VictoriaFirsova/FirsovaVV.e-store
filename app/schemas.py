from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.models import OrderStatus


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
        from_attributes = True


class ProductUpdate(ProductBase):
    pass


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    product: ProductBase

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    created_at: datetime
    status: str
    items: List[OrderItem]

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    new_status: OrderStatus


class OrderItem(OrderItem):
    product: ProductBase


class Order(Order):
    items: List[OrderItem]

