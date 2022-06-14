import uuid

from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.errors import not_found_error_response
from db.database import get_db
from db.crud import is_category_exists, create_shop_unit, get_shop_unit, delete_shop_unit

from schemas.shop_unit import ShopUnitImportRequest, ShopUnitImport, ShopUnitType

router = APIRouter()


def update_date_of_parent():
    pass


def safe_create_shop_unit(db: Session, unit: ShopUnitImport, shop_unit_dict, date):
    try:
        if unit.parentId:
            if is_category_exists(db, unit.parentId):
                create_shop_unit(db, unit, date)
            elif unit.parentId in shop_unit_dict and shop_unit_dict[unit.parentId].type == ShopUnitType.category:
                safe_create_shop_unit(db, shop_unit_dict[unit.parentId], shop_unit_dict, date)
                create_shop_unit(db, unit, date)
            else:
                raise RequestValidationError(f"There is no category with provided parentId of unit#{unit.id}")
        else:
            create_shop_unit(db, unit, date)
        del shop_unit_dict[unit.id]
    except IntegrityError as ex:
        raise RequestValidationError(f"unit#{unit.id} error. {str(ex)}")


@router.post("/imports")
async def imports(data: ShopUnitImportRequest, db: Session = Depends(get_db)):
    shop_unit_dict = {}
    for item in data.items:
        key = item.id
        if key in shop_unit_dict:
            raise RequestValidationError("All object ids in list must be unique")
        shop_unit_dict[key] = item
    while shop_unit_dict:
        safe_create_shop_unit(db, list(shop_unit_dict.values())[0], shop_unit_dict, data.updateDate)

    return Response(status_code=status.HTTP_200_OK)


@router.delete("/delete/{id}")
async def delete(id: uuid.UUID, db: Session = Depends(get_db)):
    unit = get_shop_unit(db, id)
    if unit:
        delete_shop_unit(db, unit)
        return Response(status_code=status.HTTP_200_OK)
    else:
        return not_found_error_response
