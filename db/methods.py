import datetime
import uuid

from typing import Optional

from sqlalchemy.orm import Session

from db.models import Offer, Category, ShopUnitType
from schemas import shop_unit as schemas_unit


def get_offer(db: Session, id: uuid.UUID):
    return db.query(Offer).filter(Offer.id == id).first()


def get_category(db: Session, id: uuid.UUID):
    return db.query(Category).filter(Category.id == id).first()


def get_shop_unit(db: Session, id: uuid.UUID):
    return get_category(db, id) or get_offer(db, id)


def is_category_exists(db: Session, id: uuid.UUID) -> bool:
    category = db.query(Category).filter(Category.id == id).first()
    return category is not None


def create_offer(db: Session, data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = Offer(**data.dict(exclude={"type"}), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)

    if data.parentId:
        update_unit_parents_data(db, None, db_unit.parentId, None, db_unit.price, date)

    return db_unit


def create_category(db: Session, data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = Category(**data.dict(exclude={"type"}), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)

    if data.parentId:
        update_unit_parents_data(db, None, db_unit.parentId, None, None, date)

    return db_unit


def create_shop_unit(db: Session, data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    if data.type == ShopUnitType.category:
        return create_category(db, data, date)
    elif data.type == ShopUnitType.offer:
        return create_offer(db, data, date)


def update_shop_unit(db: Session, unit: [Category, Offer], unit_import: schemas_unit.ShopUnitImport,
                     date: datetime.datetime):
    old_parent_id = unit.parentId
    old_price = unit.price if unit.type == ShopUnitType.offer else unit.summary_price

    update_dict = unit_import.dict()
    del update_dict['type']

    # Разная обработка поля price для каждого типа
    if unit.type == ShopUnitType.category:
        del update_dict['price']
        new_price = unit.summary_price
    else:
        new_price = unit_import.price

    for key, val in update_dict.items():
        setattr(unit, key, val)

    update_date_and_history(db, unit, date)

    db.commit()

    update_unit_parents_data(db, old_parent_id, unit_import.parentId, old_price, new_price, date)


def recalculate_category_price(db: Session, category: Category, date: Optional[datetime.datetime],
                               old_summary_price: int, offers_change_count: int):
    category.offers_count += offers_change_count
    children_count = category.offers_count
    if children_count:
        category.price = category.summary_price // children_count
    else:
        category.price = None
    if date:
        update_date_and_history(db, unit=category, date=date)
    db.commit()
    if category.parentId:
        update_unit_parents_data(db, category.parentId, category.parentId, old_summary_price,
                                 category.summary_price, date, offers_change_count=offers_change_count)


def update_unit_parents_data(db: Session, old_parent_id: Optional[uuid.UUID], new_parent_id: Optional[uuid.UUID],
                             old_price: Optional[int], new_price: Optional[int], date: Optional[datetime.datetime],
                             offers_change_count: int = 0):
    """
    Рекурсивно обновляет данные "вышестоящих" родительских категорий при изменении/добавлении товара,
    в частности обновляет среднюю цену по категории.
    Старое и новое состояние параметров цена, айди категории одинаково, если они не меняются у товара.

    :param db: сессия sqlalchemy
    :param old_parent_id: айди старой категории товара
    :param new_parent_id: айди новой категории товара
    :param old_price: старая цена товара
    :param new_price: новая цена товара
    :param date: дата изменения
    :param offers_change_count: число, на которое меняется общее количество товаров в категории
    :return:
    """
    if old_parent_id is None and new_parent_id is None:
        return

    if old_parent_id == new_parent_id:
        parent = get_shop_unit(db, old_parent_id)
        old_summary_price = parent.summary_price

        if old_price != new_price:
            old_price = int(old_price or 0)
            new_price = int(new_price or 0)
            parent.summary_price += (new_price - old_price)

        recalculate_category_price(db, parent, date, old_summary_price, offers_change_count)
    else:
        if old_parent_id:
            parent = get_shop_unit(db, old_parent_id)
            if old_price:
                old_summary_price = parent.summary_price
                parent.summary_price -= old_price
                recalculate_category_price(db, parent, date, old_summary_price, -1)
            elif date:
                update_date_and_history(db, parent, date)

        if new_parent_id:
            parent = get_shop_unit(db, new_parent_id)
            if new_price:
                old_summary_price = parent.summary_price
                parent.summary_price += new_price
                recalculate_category_price(db, parent, date, old_summary_price, 1)
            elif date:
                update_date_and_history(db, parent, date)
    db.commit()


def update_date_and_history(db: Session, unit: [Category, Offer], date: datetime.datetime):
    unit.date = date
    db.commit()


def create_or_update_shop_unit(db: Session, unit: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = get_shop_unit(db, unit.id)
    if db_unit:
        update_shop_unit(db, db_unit, unit, date)
    else:
        return create_shop_unit(db, unit, date)


def delete_offer(db: Session, id: uuid.UUID):
    return db.query(Offer).filter(Offer.id == id).first()


def delete_category(db: Session, id: uuid.UUID):
    return db.query(Category).filter(Category.id == id).first()


def delete_shop_unit(db: Session, unit: [Category, Offer]):
    db.delete(unit)

    if unit.parentId:
        old_price = unit.price if isinstance(unit, Offer) else unit.summary_price
        update_unit_parents_data(db, unit.parentId, None, old_price, None, None)

    db.commit()
