import asyncio
from app.db.mongo.session import mongo_db

async def clean_mongo():
    await mongo_db.users_read.delete_many({})
    await mongo_db.items_read.delete_many({})

if __name__ == "__main__":
    asyncio.run(clean_mongo())
