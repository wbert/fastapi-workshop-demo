from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, text
from app.core.db import Base


class Item(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, index=True)
    description = Column(Text, nullable=True)
    price_cents = Column(Integer, nullable=False, default=0)

    __table_args__ = tuple(UniqueConstraint("name", name="uq_items_name"))
