from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app.models import Base, Order, OrderItem, Product

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:3904@localhost/e-store"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)


def get_test_db():
    db = SessionLocal()
    try:
        yield db
        print(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")
    finally:
        db.close()


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture(scope="function")
def db():
    drop_database()
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()


def setup_test_products(db):
    products = [
        Product(name="Product 1", description="Description 1", price=100, quantity=50),
        Product(name="Product 2", description="Description 2", price=200, quantity=40),
        Product(name="Product 3", description="Description 3", price=300, quantity=30),
        Product(name="Product 4", description="Description 4", price=400, quantity=20),
        Product(name="Product 5", description="Description 5", price=500, quantity=10),
    ]
    db.add_all(products)
    db.commit()


def setup_test_orders(db):
    order1 = Order(created_at=datetime(2023, 9, 28, 14, 30, 0))
    order2 = Order(created_at=datetime(2024, 9, 30, 18, 30, 0))

    db.add(order1)
    db.add(order2)
    db.commit()
    orders = db.query(Order).all()

    item1_order1 = OrderItem(order_id=order1.id, product_id=1, quantity=20)
    item2_order1 = OrderItem(order_id=order1.id, product_id=2, quantity=10)

    item1_order2 = OrderItem(order_id=order2.id, product_id=3, quantity=15)
    item2_order2 = OrderItem(order_id=order2.id, product_id=4, quantity=5)

    db.add_all([item1_order1, item2_order1, item1_order2, item2_order2])
    db.commit()


def drop_database():
    Base.metadata.drop_all(bind=engine)


def test_get_orders(client, db):
    setup_test_products(db)
    setup_test_orders(db)
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert len(data[0]["items"]) == 2
    assert len(data[1]["items"]) == 2
    assert data[0]["items"][0]["product"]["name"] == "Product 1"


def test_create_order(client, db):
    setup_test_products(db)
    order_data = {
        "items": [
            {"product_id": 1, "quantity": 3},
            {"product_id": 2, "quantity": 4}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    order_data = {
        "items": [
            {"product_id": 40, "quantity": 3}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 404
    order_data = {
        "items": [
            {"product_id": 2, "quantity": 300}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400


def test_create_product(client, db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 10,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == product_data["name"]


def test_get_product_list(client, db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 10,
    }
    client.post("/products", json=product_data)

    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_find_product(client, db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 10,
    }
    response = client.post("/products", json=product_data)
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    response = client.get(f"/products/9999")
    assert response.status_code == 404


def test_update_product(client, db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 10,
    }
    response = client.post("/products", json=product_data)
    product_id = response.json()["id"]

    updated_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 150.0,
        "quantity": 20,
    }
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    response = client.put(f"/products/9999", json=updated_data)
    assert response.status_code == 404


def test_delete_product(client, db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 10,
    }
    response = client.post("/products", json=product_data)
    product_id = response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_read_order(client, db):
    setup_test_products(db)
    order_data = {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 3},
        ]
    }
    response = client.post("/orders", json=order_data)

    order_id = response.json()["id"]
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == order_id
    assert len(data["items"]) == 2
    assert data["items"][0]["product_id"] == 1
    assert data["items"][1]["product_id"] == 2

    response = client.get("/orders/99999")
    assert response.status_code == 404


def test_change_order_status(client, db):
    setup_test_products(db)
    setup_test_orders(db)

    order_id = 1
    new_status = {
        "new_status": "sent"
    }

    response = client.patch(f"/orders/{order_id}/status", json=new_status)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"