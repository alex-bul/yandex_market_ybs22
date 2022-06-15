import datetime
import uuid

from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from db.models import ShopUnit, ShopUnitType
from schemas import shop_unit as schemas_unit


def is_category_exists(db: Session, unit_id: uuid.UUID) -> bool:
    category = db.query(ShopUnit).filter(ShopUnit.id == unit_id, ShopUnit.type == ShopUnitType.category).first()
    return category is not None


def get_shop_unit(db: Session, unit_id: uuid.UUID) -> ShopUnit:
    return db.query(ShopUnit).filter(ShopUnit.id == unit_id).first()


def update_date_by_unit_id(db: Session, unit_id: uuid.UUID, date: datetime.datetime):
    db.execute(
        update(ShopUnit).where(ShopUnit.id == unit_id).values(date=date)
    )


def get_children_nonempty_count(db: Session, parent_id: uuid.UUID) -> int:
    return db.query(ShopUnit).filter(ShopUnit.parentId == parent_id, ShopUnit.price != None).count()


def recalculate_category_price(db: Session, category: ShopUnit, date: Optional[datetime.datetime]):
    children_count = get_children_nonempty_count(db, category.id)
    old_average_price = category.price
    if children_count:
        category.price = category.summary_price // children_count
    else:
        category.price = None
    if date:
        category.date = date
    db.commit()
    if category.parentId:
        update_unit_parents_data(db, category.parentId, category.parentId, old_average_price, category.price, date)


def create_or_update_shop_unit(db: Session, unit: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = get_shop_unit(db, unit.id)
    if db_unit:
        update_shop_unit(db, db_unit, unit, date)
    else:
        return create_shop_unit(db, unit, date)


def update_unit_parents_data(db: Session, old_parent_id: Optional[uuid.UUID], new_parent_id: Optional[uuid.UUID],
                             old_price: Optional[int], new_price: Optional[int], date: Optional[datetime.datetime]):
    if old_parent_id == new_parent_id and old_price == new_price or (old_parent_id is None and new_parent_id is None):
        return

    if old_parent_id == new_parent_id:
        old_price = int(old_price or 0)
        new_price = int(new_price or 0)

        parent = get_shop_unit(db, old_parent_id)
        parent.summary_price += (new_price - old_price)
        recalculate_category_price(db, parent, date)
    else:
        if old_parent_id:
            if old_price:
                parent = get_shop_unit(db, old_parent_id)
                parent.summary_price -= old_price
                recalculate_category_price(db, parent, date)
            elif date:
                update_date_by_unit_id(db, old_parent_id, date)

        if new_parent_id:
            if new_price:
                parent = get_shop_unit(db, new_parent_id)
                parent.summary_price += new_price
                recalculate_category_price(db, parent, date)
            elif date:
                update_date_by_unit_id(db, new_parent_id, date)
    db.commit()


def update_shop_unit(db: Session, unit: ShopUnit, unit_import: schemas_unit.ShopUnitImport, date: datetime.datetime):
    old_parent_id = unit.parentId
    old_price = unit.price

    # так как price=null у категории во входных данных, то по особому обрабатываем это поле для категорий
    update_dict = unit_import.dict()
    if unit.type == ShopUnitType.category:
        del update_dict['price']
        new_price = unit.price
    else:
        new_price = unit_import.price

    for key, val in update_dict.items():
        setattr(unit, key, val)

    db.commit()

    update_unit_parents_data(db, old_parent_id, unit_import.parentId, old_price, new_price, date)


def create_shop_unit(db: Session, unit: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = ShopUnit(**unit.dict(), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)

    if db_unit.parentId:
        update_unit_parents_data(db, None, db_unit.parentId, None, db_unit.price, date)

    return db_unit


def delete_shop_unit(db: Session, unit: ShopUnit):
    db.delete(unit)

    if unit.parentId:
        update_unit_parents_data(db, unit.parentId, None, unit.price, None, None)

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

# TODO убрать
c = {
    "items": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2"
        },
        {
            "type": "OFFER",
            "name": "Samson 70\" LED UHD Smart",
            "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
            "parentId": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
            "price": 32999
        },
        {
            "type": "CATEGORY",
            "name": "Телевизоры r",
            "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2"
        }
    ],
    "updateDate": "2022-02-03T12:00:00.000Z"
}
