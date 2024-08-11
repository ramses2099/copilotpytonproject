from typing import Optional
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


# models pydantic
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# database
DATABASE_URL = "sqlite:///test.db"


class Base(DeclarativeBase):
    pass


class DBItem(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mane: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/')
def read_root():
    return "Server is running"

    
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate) -> Item:
    with SessionLocal() as session:
        new_item = DBItem(**item.model_dump())
        session.add(new_item)
        session.commit()
        session.refresh(new_item)        
        return Item(**new_item.__dict__)

@app.get('/items/{item_id}')
def read_item(item_id: int) -> Item:
    with SessionLocal() as session:
        item = session.query(DBItem).filter(DBItem.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item(**item.__dict__)

@app.put('/item/{item_id}')
def update_item(item_id: int, item: ItemUpdate) -> Item:
    with SessionLocal() as session:
        db_item = session.query(DBItem).filter(DBItem.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.model_dump().items():
            if value is not None:
                setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
        return Item(**db_item.__dict__)

@app.delete('/item/{item_id}')
def delete_item(item_id: int) -> Item:
    with SessionLocal() as session:
        db_item = session.query(DBItem).filter(DBItem.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(db_item)
        session.commit()
        return Item(**db_item.__dict__)


