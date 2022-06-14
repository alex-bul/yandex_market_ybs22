from sqlalchemy import Enum, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base
from schemas.shop_unit import ShopUnitType


class ShopUnit(Base):
    __tablename__ = "shop_units"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    parentId = Column(UUID(as_uuid=True), ForeignKey("shop_units.id"))
    children = relationship("ShopUnit")
    type = Column(Enum(ShopUnitType), nullable=False)
    price = Column(Integer, nullable=True)
