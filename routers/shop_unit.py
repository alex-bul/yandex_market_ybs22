import datetime
import uuid

from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from core.validators import is_datetime_string_iso8601
from core.errors import not_found_error_response
from db.database import get_db
from db.methods import is_category_exists, create_or_update_shop_unit, get_shop_unit, delete_shop_unit, \
    get_offer_list_sales, get_unit_statistic

from schemas import shop_unit as schemas

router = APIRouter()


def get_parent_status(db: Session, parent_id: [uuid.UUID, None], shop_unit_dict):
    """
    Определяет и возвращает статус нахождения родительской категории в базе данных, запросе.

    :param db: сессия sqlalchemy
    :param parent_id: айди родителя
    :param shop_unit_dict: словарь, формата {"uuid элемента": *его данные в schemas.ShopUnitImport*},
        создается на основе запроса для импорта элементов /imports
    :return: str: <br/>
            'exist' - находится в базе <br/>
            'need_create' - присутствует в текущем запросе для импорта, надо создать <br/>
            'not_found' - не найден в базе, в текущем запросе для импорта
    """
    if not parent_id or is_category_exists(db, parent_id):
        return 'exist'
    elif parent_id in shop_unit_dict and shop_unit_dict[parent_id].type == schemas.ShopUnitType.category:
        return 'need_create'
    return 'not_found'


def safe_create_or_update_shop_unit(db: Session, unit: schemas.ShopUnitImport, shop_unit_dict, date):
    """
    Создаёт или обновляет объект в базе данных с учетом текущего статуса родительской категории.
    Если родитель объекта ещё не создан, то сначала создаст его, а потом исходный объект.
    При создании/обновлении элемента **удаляет его из shop_unit_dict**

    :param db: сессия sqlalchemy
    :param unit: объект
    :param shop_unit_dict: словарь, формата {"uuid элемента": *его данные в schemas.ShopUnitImport*},
        создается на основе запроса для импорта элементов /imports
    :param date: дата действия
    :return:
    """
    parent_status = get_parent_status(db, unit.parentId, shop_unit_dict)
    if parent_status == 'exist':
        create_or_update_shop_unit(db, unit, date)
    elif parent_status == 'need_create':
        safe_create_or_update_shop_unit(db, shop_unit_dict[unit.parentId], shop_unit_dict, date)
        create_or_update_shop_unit(db, unit, date)
    del shop_unit_dict[unit.id]


@router.post("/imports")
async def imports(data: schemas.ShopUnitImportRequest, db: Session = Depends(get_db)):
    shop_unit_dict = {}

    print(data)

    # проверка уникальности id всех элементов в запросе и создание
    # слова формата айди: данные, для более удобной и быстрой работы с данными
    for unit in data.items:
        key = unit.id
        if key in shop_unit_dict:
            raise RequestValidationError("All object ids in list must be unique")
        shop_unit_dict[key] = unit

    # проверка наличия родительской категории
    for unit in shop_unit_dict.values():
        if get_parent_status(db, unit.parentId, shop_unit_dict) == 'not_found':
            raise RequestValidationError(f"There is no category with provided parentId of unit#{unit.id}")

    # обрабатываем каждый объект, пока не опустеет словарь для импорта.
    # после обработки элемента он удаляется из словаря внутри функции
    while shop_unit_dict:
        safe_create_or_update_shop_unit(db, list(shop_unit_dict.values())[0], shop_unit_dict, data.updateDate)

    return Response(status_code=status.HTTP_200_OK)


@router.delete("/delete/{id}")
async def delete(id: uuid.UUID, db: Session = Depends(get_db)):
    unit = get_shop_unit(db, id)
    if unit:
        delete_shop_unit(db, unit)
        return Response(status_code=status.HTTP_200_OK)
    else:
        return not_found_error_response


@router.get("/nodes/{id}", response_model=schemas.ShopUnit)
async def nodes(id: uuid.UUID, db: Session = Depends(get_db)):
    unit = get_shop_unit(db, id)
    if unit:
        return get_shop_unit(db, id)
    else:
        return not_found_error_response


@router.get("/sales", response_model=schemas.ShopUnitStatisticResponse)
async def sales(date: str, db: Session = Depends(get_db)):
    try:
        date = datetime.datetime.strptime(is_datetime_string_iso8601(date), "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        raise RequestValidationError("invalid date format. Date must be in iso8601 format")
    items = get_offer_list_sales(db, date)
    result = {"items": items}
    return result


@router.get("/nodes/{id}/statistic", response_model=schemas.ShopUnitStatisticResponse)
async def nodes_statistic(id: uuid.UUID, date_start: str, date_end: str, db: Session = Depends(get_db)):
    try:
        date_start = datetime.datetime.strptime(is_datetime_string_iso8601(date_start), "%Y-%m-%dT%H:%M:%S.%fZ")
        date_end = datetime.datetime.strptime(is_datetime_string_iso8601(date_end), "%Y-%m-%dT%H:%M:%S.%fZ")
        if date_start >= date_end:
            raise RequestValidationError("invalid interval. date_start must be < date_end")
    except ValueError:
        raise RequestValidationError("invalid date format. Date must be in iso8601 format")

    unit = get_shop_unit(db, id)
    if not unit:
        return not_found_error_response

    items = get_unit_statistic(db, id, date_start, date_end)
    result = {"items": items}
    return result
