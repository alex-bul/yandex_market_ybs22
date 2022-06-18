from sqlalchemy import Enum, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base
from schemas.shop_unit import ShopUnitType


# class ShopUnitd(Base):
#     __tablename__ = "shop_units"
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     date = Column(DateTime(timezone=True), nullable=False)
#     parentId = Column(UUID(as_uuid=True), ForeignKey("shop_units.id", ondelete='CASCADE'))
#     children = relationship("ShopUnit",
#                             backref=backref('parent', remote_side=[id]),
#                             cascade="all, delete",
#                             passive_deletes=True)
#     type = Column(Enum(ShopUnitType), nullable=False)
#     price = Column(Integer, nullable=True)
#
#     # для расчета и хранения средней цены категории
#     summary_price = Column(Integer, nullable=False, default=0)
#     offers_count = Column(Integer, nullable=False, default=0)


class ShopUnita(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)


class Category(ShopUnita):
    __tablename__ = "categories"

    parentId = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete='CASCADE'))
    children = relationship("ShopUnit",
                            backref=backref('parent', remote_side=[id]),
                            cascade="all, delete",
                            passive_deletes=True)
    price = Column(Integer, nullable=True)

    summary_price = Column(Integer, nullable=False, default=0)
    offers_count = Column(Integer, nullable=False, default=0)


class Offer(ShopUnita):
    __tablename__ = "offers"

    parentId = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete='CASCADE'))
    price = Column(Integer, nullable=False)

