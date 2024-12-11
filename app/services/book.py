from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Book
from app.schemas.book import BookCreate, BookUpdate
from app.core.exceptions import NotFoundException


class BookService:
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_books(self, skip: int=0, limit: int=100) -> list[Book]:
        query = select(Book).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalar().all())
    
    async def get_book(self, book_id: int) -> Book:
        query = select(Book).where(Book.id == book_id)
        result = await self.session.execute(query)
        book = result.scalar_one_or_none()

        if book is None:
            raise NotFoundException(f'Автор с id {book_id} не найден')
        
        return Book
    
    async def create_Book(self, book_data: BookCreate) -> Book:
        book = Book(**book_data.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book
    
    async def update_book(self, book_id: int, book_data: BookUpdate) -> Book:
        book = await self.get_book(book_id)

        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)

        await self.session.commit()
        await self.session.refresh(book)
        return book
    
    async def delete_Book(self, book_id: int) -> None:
        book = await self.get_book(book_id)
        await self.session.delete(book)
        await self.session.commit()