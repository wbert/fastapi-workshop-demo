from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.errors import NotFoundError, ConflictError, ValidationError
from .schemas import ItemCreate, ItemRead
from .repository import ItemRepository
from .services import ItemService

router = APIRouter(prefix="/items", tags=["items"])


def get_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(ItemRepository(db))


@router.post("/", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate, svc: ItemService = Depends(get_service)):
    try:
        return svc.create_item(payload)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, svc: ItemService = Depends(get_service)):
    try:
        return svc.get_item(item_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[ItemRead])
def list_items(
    q: str | None = None,
    limit: int = 20,
    offset: int = 0,
    svc: ItemService = Depends(get_service),
):
    return svc.list_items(q=q, limit=limit, offset=offset)


@router.put("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int, payload: ItemCreate, svc: ItemService = Depends(get_service)
):
    try:
        return svc.update_item(item_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, svc: ItemService = Depends(get_service)):
    try:
        svc.delete_item(item_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
