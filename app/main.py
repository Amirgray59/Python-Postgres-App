from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.item import router as item_router
from app.api.routes.user import router as user_router
from app.api.routes.items_read import router as read_item_router
from app.utils.logging import configure_logging
from app.db.mongo.client import MongoClientManager
from app.db.mongo.session import MONGO_DB, MONGO_URL

@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo = MongoClientManager(
        uri=MONGO_URL,
        db_name=MONGO_DB,
    )
    await mongo.connect()
    app.state.mongo = mongo
    yield
    await mongo.close()


configure_logging()
app = FastAPI(lifespan=lifespan)

app.include_router(item_router)
app.include_router(user_router)
app.include_router(read_item_router)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/ready", tags=["health"])
def ready():
    return {"status": "ready"}
