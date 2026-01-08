from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional


class MongoClientManager:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self.client: Optional[AsyncIOMotorClient] = None

    async def connect(self):
        self.client = AsyncIOMotorClient(self._uri)

    async def close(self):
        if self.client:
            self.client.close()

    @property
    def db(self):
        if not self.client:
            raise RuntimeError("Mongo client not initialized")
        return self.client[self._db_name]
