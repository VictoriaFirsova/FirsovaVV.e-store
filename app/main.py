import uvicorn
from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.crud import update_order_status
from app.schemas import OrderStatusUpdate

'''from . import crud, models, schemas'''
from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


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
@app.get("/products", response_model=List[schemas.Product])
def get_product_list(db: Session = Depends(get_db)):
    return crud.get_products(db)


# Эндпоинт для получения информации о товаре по id
@app.get("/products/{id}", response_model=schemas.Product)
def find_product(id: int, db: Session = Depends(get_db)):
    return crud.get_product_by_id(db=db, product_id=id)


# Эндпоинт для обновления информации о товаре (PUT /products/{id})
@app.put("/products/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db=db, product=product, product_id=id)


# Эндпоинт для удаления товара (DELETE /products/{id})
@app.delete("/products/{id}", response_model=schemas.Product)
def delete_product(id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=id)


# Эндпоинт для создания заказа
@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)



# Эндпоинт для получения списка заказов (GET /orders).
@app.get("/orders", response_model=List[schemas.Order])
def get_order_list(db: Session = Depends(get_db)):
    return crud.get_orders(db)


# Эндпоинт для получения информации о заказе по id (GET /orders/{id}).
@app.get("/orders/{id}", response_model=schemas.Order)
def read_order(id: int, db: Session = Depends(get_db)):
    return crud.get_order_by_id(db=db, order_id=id)


# Эндпоинт для обновления статуса заказа (PATCH /orders/{id}/status).
@app.patch("/orders/{order_id}/status")
def change_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    return update_order_status(db, order_id, status_update.new_status)


if __name__ == "__main__":
    # Запуск приложения через Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
