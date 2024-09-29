from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.orm import joinedload

from .models import OrderStatus


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product_by_id(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def update_product(db: Session, product: schemas.ProductUpdate, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


def create_order(db: Session, order: schemas.OrderCreate):
    new_order = models.Order(status="in_process")

    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        if product.quantity < item.quantity:

            raise HTTPException(status_code=400,
                                detail=f"Not enough stock for product {product.id}. Available: {product.quantity}, Requested: {item.quantity}")
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        product.quantity -= item.quantity
        order_item = models.OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_item)

    db.commit()
    return new_order


def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order_by_id(db: Session, order_id: int):
    order = db.query(models.Order).options(joinedload(models.Order.items)).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.status = new_status.value
    db.commit()
    db.refresh(db_order)
    return db_order
