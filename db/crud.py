import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.models import ShopUnit, ShopUnitType
from schemas import shop_unit as schemas_unit


def is_category_exists(db: Session, unit_id: uuid.UUID):
    category = db.query(ShopUnit).filter(ShopUnit.id == unit_id, ShopUnit.type == ShopUnitType.category).first()
    return category is not None


def get_shop_unit(db: Session, unit_id: uuid.UUID):
    return db.query(ShopUnit).filter(ShopUnit.id == unit_id).first()


def create_or_update_shop_unit(db: Session, unit: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = get_shop_unit(db, unit.id)
    if db_unit:
        update_shop_unit(db, db_unit, unit, date)
    else:
        return create_shop_unit(db, unit, date)


def update_category_data_by_id(db: Session, category_id: uuid.UUID, date: datetime.datetime, old_unit_price: int,
                               new_unit_price: int):
    # TODO реализовать обновление, подсчет средней цены

    category = db.query(ShopUnit).filter(ShopUnit.id == category_id, ShopUnit.type == ShopUnitType.category).one()
    print(category)
    # update_data = schemas_unit.ShopUnitImport.from_orm(category)
    # # update_data = category.dict()
    # # update_data.pop('_sa_instance_state', None)
    # # update_data['date'] = date
    # update_shop_unit(db, category, update_data, date)
    # if category.parentId:
    #     pass


def update_shop_unit(db: Session, unit: ShopUnit, update_data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    if unit.parentId:
        update_category_data_by_id(db, unit.parentId, date, 0, 0)


def create_shop_unit(db: Session, unit: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = ShopUnit(**unit.dict(), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit


def delete_shop_unit(db: Session, unit: ShopUnit):
    db.delete(unit)
    db.commit()

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
