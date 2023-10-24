# tests/test_main.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Goto http://0.0.0.0:8000/docs to see the API documentation"

def test_create_product():
    response = client.post("/products/", json={"name": "Test Product", "price": 10.99})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_read_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_product():
    response = client.put("/products/1", json={"name": "Updated Product"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
