import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_create_user(async_client):
    email = f"test@{uuid()}.com"
    payload = {"name": "test", "email": email}
    
    response = await async_client.post("/users", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test"
    assert data["email"] == email
    assert "id" in data

@pytest.mark.asyncio
async def test_all_users(async_client):
    # First, create a user
    email = f"test@{uuid()}.com"
    payload = {"name": "test", "email": email}
    await async_client.post("/users", json=payload)

    # Fetch all users
    response = await async_client.get("/users")
    assert response.status_code == 200
    data = response.json()
    
    # At least one user should exist
    assert len(data) >= 1
    
    # Each user should have id, name, email
    for user in data:
        assert "id" in user
        assert "name" in user
        assert "email" in user
