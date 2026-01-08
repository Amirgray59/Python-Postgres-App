from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from app.db.mongo.session import mongo_db, get_mongo
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/read/items", tags=["read"])


@router.get("/")
async def read_items_by_tag(
    tag: str,
    limit: int = Query(20, ge=1, le=100),
    cursor: str | None = None,
    mongo: AsyncIOMotorDatabase = Depends(get_mongo)
):
    q = {
        "tags": {"$in": [tag]}
    }

    if cursor:
        try:
            q["_id"] = {"$gt": ObjectId(cursor)}
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid cursor")

    cursor_db = (
        mongo.items_read
        .find(q)
        .sort("_id", 1)
        .limit(limit)
    )

    results = []
    async for doc in cursor_db:
        doc["id"] = str(doc.pop("_id"))
        results.append(doc)

    next_cursor = results[-1]["id"] if results else None

    return {
        "items": results,
        "next_cursor": next_cursor,
    }
