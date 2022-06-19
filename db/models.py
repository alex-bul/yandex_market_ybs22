from sqlalchemy import Enum, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base
from schemas.shop_unit import ShopUnitType


class ShopUnit(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)


class Category(ShopUnit):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)

    parentId = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete='CASCADE'))
    children_category = relationship("Category",
                                     backref=backref('parent', remote_side="Category.id"),
                                     cascade="all, delete",
                                     passive_deletes=True)
    children_offer = relationship("Offer",
                                  backref=backref('parent', remote_side="Category.id"),
                                  cascade="all, delete",
                                  passive_deletes=True)

    price = Column(Integer, nullable=True)

    summary_price = Column(Integer, nullable=False, default=0)
    offers_count = Column(Integer, nullable=False, default=0)

    type = ShopUnitType.category

    @property
    def children(self):
        return self.children_category + self.children_offer


class Offer(ShopUnit):
    __tablename__ = "offers"

    parentId = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete='CASCADE'))
    price = Column(Integer, nullable=False)

    type = ShopUnitType.offer
