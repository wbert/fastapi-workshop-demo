from sqlalchemy.exc import IntegrityError
from .repository import ItemRepository
from app.core.errors import NotFoundError, ConflictError, ValidationError
from .schemas import ItemCreate
from .models import Item


class ItemService:
    """Business rules & orchestration (no SQL here)."""

    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def create_item(self, payload: ItemCreate) -> Item:
        # Example domain rule: enforce unique name with friendly error
        try:
            return self.repo.create(
                name=payload.name,
                description=payload.description,
                price_cents=payload.price_cents,
            )
        except IntegrityError:
            raise ConflictError("Item name must be unique")

    def get_item(self, item_id: int) -> Item:
        obj = self.repo.get(item_id)
        if not obj:
            raise NotFoundError("Item not found")
        return obj

    def list_items(self, *, q: str | None, limit: int, offset: int):
        return self.repo.list(q=q, limit=limit, offset=offset)

    def update_item(self, item_id: int, payload: ItemCreate) -> Item:
        try:
            obj = self.repo.update(
                item_id,
                name=payload.name,
                description=payload.description,
                price_cents=payload.price_cents,
            )
        except IntegrityError:
            raise ConflictError("Item name must be unique")
        if not obj:
            raise NotFoundError("Item not found")
        return obj

    def delete_item(self, item_id: int) -> None:
        ok = self.repo.delete(item_id)
        if not ok:
            raise NotFoundError("Item not found")
