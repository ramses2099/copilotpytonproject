import pytest
from src.main import SessionLocal
from src.operations import *


@pytest.fixture
def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
     

def test_create_item(session: Session) -> None:
    item = db_create_item(ItemCreate(name= "Foo", description="An item"),
        session)
    assert item is not None
    assert item.id is not None
    assert item.name == "Foo"
    assert item.description == "An item"
    
def test_read_item(session: Session) -> None:
    item = db_create_item(ItemCreate(name= "Bar", description="Another item"),
        session)
    item_from_db = db_read_item(item.id, session)
    assert item_from_db is not None
    assert item_from_db.id == item.id
    assert item_from_db.name == "Bar"
    assert item_from_db.description == "Another item"