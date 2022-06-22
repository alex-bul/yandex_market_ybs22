import datetime
import uuid

from typing import Optional

from sqlalchemy.orm import Session

from db.models import Offer, Category, ShopUnitType, ShopUnitHistory
from schemas import shop_unit as schemas_unit


def get_offer(db: Session, id: uuid.UUID):
    return db.query(Offer).filter(Offer.id == id).first()


def get_category(db: Session, id: uuid.UUID):
    return db.query(Category).filter(Category.id == id).first()


def get_shop_unit(db: Session, id: uuid.UUID):
    return get_category(db, id) or get_offer(db, id)


def get_offer_list_sales(db: Session, date_end: datetime.datetime):
    date_start = date_end - datetime.timedelta(hours=24)
    history_rows = db.query(ShopUnitHistory.id).filter(ShopUnitHistory.date > date_start).filter(
        ShopUnitHistory.date < date_end).filter(ShopUnitHistory.type == ShopUnitType.offer).filter(
        ShopUnitHistory.is_object_creation == False).distinct(
        ShopUnitHistory.id).all()
    return [get_offer(db, row[0]) for row in history_rows]


def get_unit_statistic(db: Session, id: uuid.UUID, date_start: datetime.datetime, date_end: datetime.datetime):
    r = db.query(ShopUnitHistory).filter(ShopUnitHistory.id == id)
    if date_start:
        r = r.filter(ShopUnitHistory.date > date_start)
    if date_end:
        r = r.filter(ShopUnitHistory.date > date_end)
    return r.all()


def is_category_exists(db: Session, id: uuid.UUID) -> bool:
    category = db.query(Category).filter(Category.id == id).first()
    return category is not None


def create_offer(db: Session, data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = Offer(**data.dict(exclude={"type"}), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)

    if data.parentId:
        update_unit_parents_data(db, old_parent_id=None, new_parent_id=db_unit.parentId, old_price=None,
                                 new_price=db_unit.price, date=date)

    return db_unit


def create_category(db: Session, data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = Category(**data.dict(exclude={"type"}), date=date)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)

    if data.parentId:
        update_unit_parents_data(db, old_parent_id=None, new_parent_id=db_unit.parentId, old_price=None,
                                 new_price=db_unit.price, date=date)

    return db_unit


def create_shop_unit(db: Session, data: schemas_unit.ShopUnitImport, date: datetime.datetime):
    if data.type == ShopUnitType.category:
        unit = create_category(db, data, date)
    elif data.type == ShopUnitType.offer:
        unit = create_offer(db, data, date)
    else:
        raise ValueError("invalid shop unit type")
    update_date_and_history(db, unit, date, is_object_creation=True)

    return unit


def create_shop_unit_history(db: Session, db_unit: [Category, Offer], is_object_creation=False):
    unit = schemas_unit.ShopUnit.from_orm(db_unit)
    history_object = db.query(ShopUnitHistory).filter(ShopUnitHistory.id == unit.id).filter(
        ShopUnitHistory.date == unit.date).first()
    if history_object:
        for key, val in unit.dict().items():
            setattr(history_object, key, val)
    else:
        history_object = ShopUnitHistory(**unit.dict(include={"id", "type", "name", "parentId", "price", "date"}),
                                         is_object_creation=is_object_creation)
        db.add(history_object)
    db.commit()
    db.refresh(history_object)

    return history_object


def update_shop_unit(db: Session, unit: [Category, Offer], unit_import: schemas_unit.ShopUnitImport,
                     date: datetime.datetime):
    old_parent_id = unit.parentId

    update_dict = unit_import.dict()
    del update_dict['type']

    # Разная обработка поля price для каждого типа
    if isinstance(unit, Category):
        del update_dict['price']

        # при обновлении категории средняя цена не меняется
        old_price = unit.summary_price
        new_price = unit.summary_price
    else:
        old_price = unit.price
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
                recalculate_category_price(db, parent, date, old_summary_price, offers_change_count=-1)
            elif date:
                update_date_and_history(db, parent, date)

        if new_parent_id:
            parent = get_shop_unit(db, new_parent_id)
            if new_price:
                old_summary_price = parent.summary_price
                parent.summary_price += new_price
                recalculate_category_price(db, parent, date, old_summary_price, offers_change_count=1)
            elif date:
                update_date_and_history(db, parent, date)
    db.commit()


def update_date_and_history(db: Session, unit: [Category, Offer], date: datetime.datetime, is_object_creation=False):
    unit.date = date
    create_shop_unit_history(db, unit, is_object_creation)
    db.commit()


def create_or_update_shop_unit(db: Session, unit: schemas_unit.ShopUnitImport, date: datetime.datetime):
    db_unit = get_shop_unit(db, unit.id)
    if db_unit:
        update_shop_unit(db, db_unit, unit, date)
    else:
        delete_history_by_shop_unit_id(db, unit.id)
        return create_shop_unit(db, unit, date)


def delete_history_by_shop_unit_id(db: Session, unit_id: uuid.UUID):
    return db.query(ShopUnitHistory).filter(ShopUnitHistory.id == unit_id).delete()


def delete_shop_unit(db: Session, unit: [Category, Offer]):
    db.delete(unit)

    if unit.parentId:
        old_price = unit.price if isinstance(unit, Offer) else unit.summary_price
        update_unit_parents_data(db, unit.parentId, None, old_price, None, None)

    db.commit()
