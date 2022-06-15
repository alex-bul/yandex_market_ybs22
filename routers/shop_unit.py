import uuid

from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.errors import not_found_error_response
from db.database import get_db
from db.crud import is_category_exists, create_or_update_shop_unit, get_shop_unit, delete_shop_unit, create_shop_unit

from schemas.shop_unit import ShopUnitImportRequest, ShopUnitImport, ShopUnitType

router = APIRouter()


def update_date_of_parent():
    pass


def get_parent_status(db: Session, parent_id: [uuid.UUID, None], shop_unit_dict):
    if not parent_id or is_category_exists(db, parent_id):
        return 'exist'
    elif parent_id in shop_unit_dict and shop_unit_dict[parent_id].type == ShopUnitType.category:
        return 'need_create'
    return 'not_found'


def safe_create_or_update_shop_unit(db: Session, unit: ShopUnitImport, shop_unit_dict, date):
    parent_status = get_parent_status(db, unit.parentId, shop_unit_dict)
    if parent_status == 'exist':
        create_or_update_shop_unit(db, unit, date)
    elif parent_status == 'need_create':
        safe_create_or_update_shop_unit(db, shop_unit_dict[unit.parentId], shop_unit_dict, date)
        create_or_update_shop_unit(db, unit, date)
    del shop_unit_dict[unit.id]


@router.post("/imports")
async def imports(data: ShopUnitImportRequest, db: Session = Depends(get_db)):
    shop_unit_dict = {}

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
