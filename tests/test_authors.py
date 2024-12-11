import pytest
from datetime import date
from httpx import AsyncClient

from app.models.models import Author


@pytest.mark.asyncio
async def test_create_author(client: AsyncClient):
    response = await client.post(
        "/api/v1/authors",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": str(date(1990, 1, 1))
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


@pytest.mark.asyncio
async def test_get_author(client: AsyncClient, test_author: Author):
    response = await client.get(f"/api/v1/authors/{test_author.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_author.first_name
    assert data["last_name"] == test_author.last_name


@pytest.mark.asyncio
async def test_update_author(client: AsyncClient, test_author: Author):
    response = await client.put(
        f"/api/v1/authors/{test_author.id}",
        json={
            "first_name": "Updated",
            "last_name": "Author",
            "birth_date": str(date(1990, 1, 1))
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_author(client: AsyncClient, test_author: Author):
    response = await client.delete(f"/api/v1/authors/{test_author.id}")
    assert response.status_code == 204