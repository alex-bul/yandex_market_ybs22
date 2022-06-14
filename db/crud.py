import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.models import ShopUnit, ShopUnitType
from schemas import shop_unit


def is_category_exists(db: Session, unit_id: uuid.UUID):
    # print(select(ShopUnit).filter(ShopUnit.id == unit_id, ShopUnit.type == ShopUnitType.category).exists())
    return db.query(select(ShopUnit).filter(ShopUnit.id == unit_id, ShopUnit.type == ShopUnitType.category).exists())


def get_shop_unit(db: Session, unit_id: uuid.UUID):
    return db.query(ShopUnit).filter(ShopUnit.id == unit_id).first()


# def get_shop_unit_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()


# def get_shop_units(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()


def create_shop_unit(db: Session, unit: shop_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = ShopUnit(**unit.dict(), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
