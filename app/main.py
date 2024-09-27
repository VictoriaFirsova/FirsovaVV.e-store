from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт для создания товара
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


# Эндпоинт для получения списка товаров
@app.get("/products", response_model= List[schemas.Product])
def get_product_list(skip: int = 0, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip)
    return products


# Эндпоинт для получения информации о товаре по id
@app.get("/products/{id}", response_model=schemas.Product)
def find_product(id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db=db, product_id=id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Эндпоинт для обновления информации о товаре (PUT /products/{id})
@app.put("/products/{id}", response_model=schemas.Product)
def update_product(id: int, product_update: schemas.ProductBase, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_update.name
    product.description = product_update.description
    product.price = product_update.price
    product.quantity = product_update.quantity

    db.commit()
    db.refresh(product)

    return product


# Эндпоинт для удаления товара (DELETE /products/{id})
@app.delete("/products/{id}", response_model=schemas.Product)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return product


# Эндпоинт для создания заказа
@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order()
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order