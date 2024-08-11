from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session 
from .operations import (
    Base,
    Item,
    ItemCreate,
    ItemUpdate,
    NotFoundError,
    db_create_item,
    db_update_item,
    db_read_item,
    db_delete_item)

# database
DATABASE_URL = "sqlite:///test.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# depenency to get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


@app.get('/')
def read_root():
    return "Server is running"

    
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    return db_create_item(item, db)


@app.get('/items/{item_id}')
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        return db_read_item(item_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
    

@app.put('/items/{item_id}', response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    try:
        return db_update_item(item_id, item, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
    

@app.delete('/item/{item_id}')
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        return db_delete_item(item_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
   


