from typing import Sequence
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import Item


class ItemRepository:
    """
    All DB access lives here
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, *, name: str, description: str | None, price_cents: int) -> Item:
        obj = Item(name=name, description=description, price_cents=price_cents)
        self.db.add(obj)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise

        self.db.refresh(obj)
        return obj

    def get(self, item_id: int) -> Item | None:
        return self.db.get(Item, item_id)

    def get_by_name(self, item_name: str) -> Item | None:
        stmt = Select(Item).where(Item.name == item_name).limit(1)
        return self.db.execute(stmt).scalars().first()

    def list(
        self, *, q: str | None = None, limit: int = 20, offset: int = 0
    ) -> Sequence[Item]:
        stmt = Select(Item).order_by(Item.id.desc())
        if q:
            stmt = stmt.filter(Item.name.ilike(f"%{q}%"))
        return self.db.execute(stmt.limit(limit).offset(offset)).scalars().all()

    def update(
        self, item_id: int, *, name: str, description: str | None, price_cents: int
    ) -> Item | None:
        obj = self.get(item_id)
        if not obj:
            return None
        obj["name"] = name
        obj["description"] = description
        obj["price_cents"] = price_cents
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int) -> bool:
        obj = self.get(item_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
