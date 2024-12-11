import pytest
from httpx import AsyncClient

from app.models.models import Book, Author


@pytest.mark.asyncio
async def test_create_book(client: AsyncClient, test_author: Author):
    response = await client.post(
        "/api/v1/books",
        json={
            "title": "New Book",
            "description": "Description",
            "available_copies": 5,
            "author_id": test_author.id
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Book"
    assert data["available_copies"] == 5
    assert data["author_id"] == test_author.id


@pytest.mark.asyncio
async def test_get_book(client: AsyncClient, test_book: Book):
    response = await client.get(f"/api/v1/books/{test_book.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_book.title
    assert data["available_copies"] == test_book.available_copies


@pytest.mark.asyncio
async def test_update_book(client: AsyncClient, test_book: Book):
    response = await client.put(
        f"/api/v1/books/{test_book.id}",
        json={
            "title": "Updated Book",
            "description": "Updated Description",
            "available_copies": 10,
            "author_id": test_book.author_id
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Book"
    assert data["available_copies"] == 10


@pytest.mark.asyncio
async def test_delete_book(client: AsyncClient, test_book: Book):
    response = await client.delete(f"/api/v1/books/{test_book.id}")
    assert response.status_code == 204