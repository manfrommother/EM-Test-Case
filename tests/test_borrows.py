import pytest
from datetime import date
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Book, Borrow


@pytest.mark.asyncio
async def test_create_borrow(client: AsyncClient, test_book: Book):
    response = await client.post(
        "/api/v1/borrows",
        json={
            "reader_name": "John Reader",
            "book_id": test_book.id
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["reader_name"] == "John Reader"
    assert data["book_id"] == test_book.id
    assert data["return_date"] is None


@pytest.mark.asyncio
async def test_get_borrow(client: AsyncClient, test_borrow: Borrow):
    response = await client.get(f"/api/v1/borrows/{test_borrow.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["reader_name"] == test_borrow.reader_name
    assert data["book_id"] == test_borrow.book_id


@pytest.mark.asyncio
async def test_return_book(client: AsyncClient, test_borrow: Borrow):
    return_date = date.today().isoformat()
    response = await client.patch(
        f"/api/v1/borrows/{test_borrow.id}/return",
        json={"return_date": return_date}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["return_date"] == return_date


@pytest.mark.asyncio
async def test_cannot_borrow_unavailable_book(
    client: AsyncClient,
    test_book: Book,
    session: AsyncSession
):
    # Set available copies to 0
    test_book.available_copies = 0
    session.add(test_book)
    await session.commit()

    response = await client.post(
        "/api/v1/borrows",
        json={
            "reader_name": "John Reader",
            "book_id": test_book.id
        }
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "No available copies" in data["detail"]