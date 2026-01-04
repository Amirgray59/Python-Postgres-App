import pytest

@pytest.mark.asyncio
async def test_create_item(async_client):
    payload = {"name": "test_item", "sell_in": 5, "quality": 10, "owner_id": 1, "tags": ["tag1","tag2"]}
    response = await async_client.post("/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test_item"
    assert data["owner"]["name"] == "Alice"
    assert "id" in data
    assert data["tags"] == ["tag1","tag2"]

@pytest.mark.asyncio
async def test_get_item(async_client):
    # ابتدا یک آیتم بساز
    payload = {"name": "item_for_get", "sell_in": 3, "quality": 5, "owner_id": 1, "tags": ["t1"]}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    # سپس آن را دریافت کن
    response = await async_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "item_for_get"
    assert data["owner"]["name"] == "Alice"

@pytest.mark.asyncio
async def test_get_all_items(async_client):
    # ایجاد چند آیتم
    for i in range(3):
        payload = {"name": f"item{i}", "sell_in": i, "quality": i*10, "owner_id": 1, "tags": []}
        await async_client.post("/items", json=payload)

    response = await async_client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # حداقل سه آیتم وجود دارد

@pytest.mark.asyncio
async def test_update_item(async_client):
    # ایجاد آیتم
    payload = {"name": "old_name", "sell_in": 5, "quality": 5, "owner_id": 1, "tags": ["old"]}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    # آپدیت آیتم
    update_payload = {"name": "new_name", "sell_in": 10, "quality": 15, "tags": ["new1","new2"]}
    response = await async_client.put(f"/items/{item_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "new_name"
    assert data["sell_in"] == 10
    assert data["tags"] == ["new1","new2"]

@pytest.mark.asyncio
async def test_delete_item(async_client):
    payload = {"name": "to_delete", "sell_in": 5, "quality": 5, "owner_id": 1, "tags": []}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    response = await async_client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data["detail"]

    # بعد از حذف، دسترسی به آیتم 404 شود
    get_resp = await async_client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404