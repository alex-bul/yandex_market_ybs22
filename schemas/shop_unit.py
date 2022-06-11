import datetime
import uuid

from enum import Enum
from typing import List, ForwardRef

from pydantic import BaseModel, Field


class ShopUnitType(str, Enum):
    """
        Тип элемента - категория или товар
    """
    category = "CATEGORY"
    offer = "OFFER"


class ShopUnitBase(BaseModel):
    id: uuid.UUID = Field(description="Уникальный идентфикатор",
                          example="3fa85f64-5717-4562-b3fc-2c963f66a333",
                          nullable=False)
    name: str = Field(description="Имя категории",
                      nullable=False)
    parentId: uuid.UUID = Field(default=None,
                                description="UUID родительской категории",
                                example="3fa85f64-5717-4562-b3fc-2c963f66a333",
                                nullable=True)
    type: ShopUnitType
    price: int = Field(default=None,
                       description="Целое число, для категории - это средняя цена всех дочерних "
                                   "товаров(включая товары подкатегорий). Если цена является не целым числом, "
                                   "округляется в меньшую сторону до целого числа. Если категория не содержит "
                                   "товаров цена равна null.",
                       nullable=True)


class ShopUnit(ShopUnitBase):
    """
    Объект товара/категории
    """
    date: datetime.datetime = Field(description="Время последнего обновления элемента.",
                                    nullable=False,
                                    example="2022-05-28T21:12:01.000Z")
    children: List[ForwardRef('ShopUnit')] = Field(default=None,
                                                   description="Список всех дочерних товаров/категорий. "
                                                               "Для товаров поле равно null.")


class ShopUnitImport(ShopUnitBase):
    """
    Объект товара/категории при импорте
    """
    pass


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime.datetime = Field(description="Время обновления добавляемых товаров/категорий.",
                                          nullable=False,
                                          example="2022-05-28T21:12:01.000Z")


class ShopUnitStatisticUnit(ShopUnitBase):
    date: datetime.datetime = Field(description="Время последнего обновления элемента.",
                                    nullable=False,
                                    example="2022-05-28T21:12:01.000Z")


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit] = Field(description="История в произвольном порядке.")


ShopUnit.update_forward_refs()
