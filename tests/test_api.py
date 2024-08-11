import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
        
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running"
    
def test_create_item(client):
    response = client.post("/items", json={"name":"Foo", "description":"An item"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["description"] == "An item"
    assert "id" in data
    
    
def test_read_item(client):
    item_id = 1
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Bar"
    assert data["description"] == "An updated item"

def test_update_item(client):
    item_id = 1
    response = client.put(f"/items/{item_id}",json={"name":"Bar","description":"An updated item"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Bar"
    assert data["description"] == "An updated item"
    
    

