from typing import Optional
from pydantic import BaseModel
from sqlalchemy import  String, Integer
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

class NotFoundError(Exception):
    pass

# models pydantic
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class Base(DeclarativeBase):
    pass


class DBItem(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]


def db_find_item(item_id: int, sesseion: Session) -> DBItem:
    db_item = sesseion.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise NotFoundError("Item not found")
    return db_item

def db_create_item(item: ItemCreate, sesseion: Session) -> Item:
    db_item = DBItem(**item.model_dump())
    sesseion.add(db_item)
    sesseion.commit()
    sesseion.refresh(db_item)
    return Item(**db_item.__dict__)

def db_read_item(item_id: int, sesseion: Session) -> Item:
    db_item = db_find_item(item_id, sesseion)
    return Item(**db_item.__dict__)

def db_update_item(item_id: int, item: ItemUpdate, sesseion: Session) -> Item:
    db_item = db_find_item(item_id, sesseion)
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)    
    sesseion.commit()
    sesseion.refresh(db_item)
    return Item(**db_item.__dict__)

def db_delete_item(item_id: int, sesseion: Session) -> Item:
    db_item = db_find_item(item_id, sesseion)
    sesseion.delete(db_item)
    sesseion.commit()
    return Item(**db_item.__dict__)

