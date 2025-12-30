from fastapi import APIRouter, Depends, Response, status
from typing import Dict
import uuid

from app.domain.models import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)
from app.domain.errors import invalid_type, item_not_found
from app.api.deps import get_db, FakeDB


router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemResponse,
)
def create_item(
    item: ItemCreate,
    response: Response,
    db: FakeDB = Depends(get_db),
):
    item_id = str(uuid.uuid4())

    created = ItemResponse(
        id=item_id,
        name=item.name,
        sell_in=item.sell_in,
        quality=item.quality,
    )

    db[item_id] = created
    response.headers["Location"] = f"/items/{item_id}"
    return created


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
def get_item(
    item_id: str,
    db: FakeDB = Depends(get_db),
):
    item = db.get(item_id)
    if not item:
        return item_not_found(item_id)
    return item


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
)
def update_item(
    item_id: str,
    payload: ItemUpdate,
    db: FakeDB = Depends(get_db),
):
    item = db.get(item_id)
    if not item:
        return item_not_found(item_id)

    data = item.dict()

    if payload.sell_in is not None:
        data["sell_in"] = payload.sell_in

    if payload.quality is not None:
        data["quality"] = payload.quality

    updated = ItemResponse(**data)
    db[item_id] = updated
    return updated


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    item_id: str,
    db: FakeDB = Depends(get_db),
):
    if item_id not in db:
        return item_not_found(item_id)

    del db[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
