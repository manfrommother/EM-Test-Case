from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Borrow
from app.schemas.borrow import BorrowCreate, BorrowUpdate
from app.core.exceptions import NotFoundException, BadRequestException, NoAvailableCopiesException
from app.services.book import BookService


class BorrowService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.book_service = BookService(session)

    async def get_borrows(self, skip: int = 0, limit: int = 100) -> list[Borrow]:
        query = select(Borrow).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_borrow(self, borrow_id: int) -> Borrow:
        query = select(Borrow).where(Borrow.id == borrow_id)
        result = await self.session.execute(query)
        borrow = result.scalar_one_or_none()
        
        if borrow is None:
            raise NotFoundException(f"Borrow record with id {borrow_id} not found")
        
        return borrow

    async def create_borrow(self, borrow_data: BorrowCreate) -> Borrow:
        book = await self.book_service.get_book(borrow_data.book_id)
        if book.available_copies <= 0:
            raise NoAvailableCopiesException()

        borrow = Borrow(
            reader_name=borrow_data.reader_name,
            book_id=borrow_data.book_id,
            borrow_date=date.today()
        )
        
        self.session.add(borrow)
        await self.session.commit()
        await self.session.refresh(borrow)

        await self.book_service.update_available_copies(book.id, -1)
        
        return borrow

    async def return_book(self, borrow_id: int, return_data: BorrowUpdate) -> Borrow:
        borrow = await self.get_borrow(borrow_id)
        
        if borrow.return_date is not None:
            raise BadRequestException("This book has already been returned")
        
        borrow.return_date = return_data.return_date
        await self.session.commit()
        await self.session.refresh(borrow)
        
        await self.book_service.update_available_copies(borrow.book_id, 1)
        
        return borrow
        