import uvicorn
from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.crud import update_order_status
from app import crud, models, schemas
from app.database import SessionLocal, engine

# Initialize database and create tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(debug=True)


def get_db():
    """
    Dependency to provide a database session.
    Ensures that the session is properly closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    return crud.create_product(db=db, product=product)


@app.get("/products", response_model=List[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    """
    Get a list of all products.
    """
    return crud.get_products(db)


@app.get("/products/{id}", response_model=schemas.Product)
def get_product(id: int, db: Session = Depends(get_db)):
    """
    Get details of a product by its ID.
    """
    return crud.get_product_by_id(db=db, product_id=id)


@app.put("/products/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """
    Update product details by its ID.
    """
    return crud.update_product(db=db, product=product, product_id=id)


@app.delete("/products/{id}", response_model=schemas.Product)
def delete_product(id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.
    """
    return crud.delete_product(db=db, product_id=id)


@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    """
    return crud.create_order(db=db, order=order)


@app.get("/orders", response_model=List[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    """
    Get a list of all orders.
    """
    return crud.get_orders(db)


@app.get("/orders/{id}", response_model=schemas.Order)
def get_order(id: int, db: Session = Depends(get_db)):
    """
    Get details of an order by its ID.
    """
    return crud.get_order_by_id(db=db, order_id=id)


@app.patch("/orders/{order_id}/status")
def update_order_status_endpoint(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    """
    Update the status of an order by its ID.
    """
    return update_order_status(db, order_id, status_update.new_status)


if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
