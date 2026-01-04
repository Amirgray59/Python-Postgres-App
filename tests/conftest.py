import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def async_client(monkeypatch):
    """
    Provides an AsyncClient for tests with mocked MongoDB and Postgres session.
    """
    # ---- In-memory fake MongoDB ----
    items_store = {}
    users_store = {1: {"_id": 1, "name": "Alice", "email": "alice@example.com"}}

    # Mock users_read
    fake_users = AsyncMock()
    async def fake_find_one_user(query):
        return users_store.get(query["_id"])
    fake_users.find_one.side_effect = fake_find_one_user

    # Mock items_read
    fake_items = AsyncMock()


    
    async def fake_find_one_item(query):
        orig = items_store.get(query["_id"])
        if not orig:
            return None
        # return a copy so endpoint can modify it safely
        item = orig.copy()
        if "_id" not in item and "id" in item:
            item["_id"] = item["id"]
        if "id" not in item and "_id" in item:
            item["id"] = item["_id"]
        return item

    async def fake_insert_one(item):
        # always set _id
        if "id" in item and "_id" not in item:
            item["_id"] = item.pop("id")
        elif "_id" not in item:
            # assign a new _id if none provided
            item["_id"] = max(items_store.keys(), default=10000) + 1
        items_store[item["_id"]] = item
        return item

    async def fake_to_list(limit=None):
        # make sure each item has _id internally
        for item in items_store.values():
            if "_id" not in item and "id" in item:
                item["_id"] = item.pop("id")
        return list(items_store.values())[:limit]


    async def fake_update_one(query, update, upsert=False):
        _id = query["_id"]
        if _id in items_store:
            for k, v in update.get("$set", {}).items():
                items_store[_id][k] = v
        elif upsert:
            items_store[_id] = update.get("$set", {})
            items_store[_id]["_id"] = _id
    async def fake_delete_one(query):
        _id = query["_id"]
        if _id in items_store:
            del items_store[_id]

    fake_items.find_one.side_effect = fake_find_one_item
    fake_items.insert_one.side_effect = fake_insert_one
    fake_items.update_one.side_effect = fake_update_one
    fake_items.delete_one.side_effect = fake_delete_one

    # Patch mongo_db in router
    monkeypatch.setattr("app.api.routes.item.mongo_db.users_read", fake_users)
    monkeypatch.setattr("app.api.routes.item.mongo_db.items_read", fake_items)

    class FakeCursor:
        def __init__(self, items):
            self.items = items

        async def to_list(self, length=None):
            # return items up to `length` and ensure _id exists
            results = []
            for item in list(self.items.values())[:length]:
                # Make a copy to avoid modifying the store
                i = item.copy()
                if "_id" not in i and "id" in i:
                    i["_id"] = i["id"]
                results.append(i)
            return results


    # Instead of async def fake_find(...), just return the cursor immediately
    def fake_find(query=None):
        return FakeCursor(items_store)

    # Patch find
    fake_items.find = fake_find


    # ---- Fake Postgres session ----
    class FakeSession:
        def __init__(self):
            self.items = {}
            self.tags = {}
            self.next_id = 1

        def add(self, obj):
            if hasattr(obj, "id") and obj.id is None:
                obj.id = self.next_id
                self.next_id += 1
            if obj.__class__.__name__ == "Item":
                self.items[obj.id] = obj
            elif obj.__class__.__name__ == "Tag":
                self.tags.setdefault(obj.item_id, []).append(obj)

        def add_all(self, objs):
            for obj in objs:
                self.add(obj)

        def commit(self):
            pass

        def refresh(self, obj):
            pass

        def query(self, model):
            class Query:
                def __init__(self, session, model):
                    self.session = session
                    self.model = model

                def filter(self, condition):
                    class Filter:
                        def __init__(self, session):
                            self.session = session

                        def first(self):
                            # Simplified: return first matching item
                            if self.session.items:
                                return list(self.session.items.values())[0]
                            return None

                        def delete(self):
                            # remove all tags
                            self.session.tags.clear()
                    return Filter(self.session)
            return Query(self, model)

        def delete(self, obj):
            if obj.id in self.items:
                del self.items[obj.id]

    monkeypatch.setattr("app.api.routes.item.get_db", lambda: FakeSession())

    # ---- AsyncClient with ASGITransport ----
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
