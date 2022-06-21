import datetime
import uuid

from enum import Enum
from typing import List, ForwardRef, Literal, Optional

from pydantic import BaseModel, Field, validator, constr, conint

from core.utils import convert_datetime_to_iso_8601_with_z_suffix_and_utc
from core.validators import is_datetime_string_iso8601


class ShopUnitType(str, Enum):
    """
        Тип элемента - категория или товар
    """
    category = "CATEGORY"
    offer = "OFFER"


class ShopUnitBase(BaseModel):
    id: uuid.UUID = Field(description="Уникальный идентификатор",
                          example="3fa85f64-5717-4562-b3fc-2c963f66a333",
                          nullable=False)
    name: constr(strict=True, min_length=1) = Field(description="Имя категории/товара",
                                                    nullable=False)
    parentId: uuid.UUID = Field(default=None,
                                description="UUID родительской категории",
                                example="3fa85f64-5717-4562-b3fc-2c963f66a333",
                                nullable=True)
    type: ShopUnitType = Field(example=ShopUnitType.offer)

    price: conint(strict=True) = Field(default=None,
                                       description="Целое число, для категории - это средняя цена всех дочерних "
                                                   "товаров(включая товары подкатегорий). "
                                                   "Если цена является не целым числом, "
                                                   "округляется в меньшую сторону до целого числа. "
                                                   "Если категория не содержит "
                                                   "товаров цена равна null.",
                                       nullable=True)

    class Config:
        json_encoders = {
            datetime.datetime: convert_datetime_to_iso_8601_with_z_suffix_and_utc
        }


class ShopUnit(ShopUnitBase):
    date: datetime.datetime = Field(description="Время последнего обновления элемента.",
                                    nullable=False,
                                    example="2022-05-28T21:12:01.000Z")
    children: List[ForwardRef('ShopUnit')] = Field(default=None,
                                                   description="Список всех дочерних товаров/категорий. "
                                                               "Для товаров поле равно null.",
                                                   nullable=True)

    @validator("children")
    def children_depend_on_type(cls, v, values):
        unit_type = values.get('type', None)
        if unit_type == ShopUnitType.offer:
            if v:
                raise ValueError('offer cant have children')
            return None
        return v

    class Config:
        orm_mode = True


class ShopUnitImport(ShopUnitBase):
    """
    Объект товара/категории при импорте
    """

    @validator("price", always=True)
    def price_depend_on_type(cls, v, values):
        unit_type = values.get('type', None)
        if unit_type == ShopUnitType.category:
            if v is None:
                return v
            raise ValueError('category price must be null')
        elif unit_type == ShopUnitType.offer:
            if isinstance(v, int) and v >= 0:
                return v
            raise ValueError('offer price must be >= 0')


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime.datetime = Field(description="Время обновления добавляемых товаров/категорий.",
                                          nullable=False,
                                          example="2022-05-28T21:12:01.000Z")

    @validator("updateDate", pre=True, always=True)
    def check_update_date_format(cls, v):
        return is_datetime_string_iso8601(v)


class ShopUnitStatisticUnit(ShopUnitBase):
    date: datetime.datetime = Field(description="Время последнего обновления элемента.",
                                    nullable=False,
                                    example="2022-05-28T21:12:01.000Z")


# TODO проверка даты на iso в скидках и истории

class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit] = Field(description="История в произвольном порядке.")


ShopUnit.update_forward_refs()
