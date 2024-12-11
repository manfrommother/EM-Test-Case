from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book import BookService

router = APIRouter(prefix="/books")


@router.get("", response_model=List[Book])
async def get_books(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """Получает список книг"""
    service = BookService(session)
    return await service.get_books(skip=skip, limit=limit)


@router.post("", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_session)
):
    """Создает новую книгу"""
    service = BookService(session)
    return await service.create_book(book_data)


@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Получает книгу по ID"""
    service = BookService(session)
    return await service.get_book(book_id)


@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Обновляет информацию о книгах"""
    service = BookService(session)
    return await service.update_book(book_id, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Удаляет книги"""
    service = BookService(session)
    await service.delete_book(book_id)