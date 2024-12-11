from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Author
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.core.exceptions import NotFoundException


class AuthorService:
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_authors(self, skip: int=0, limit: int=100) -> list[Author]:
        query = select(Author).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalar().all())
    
    async def get_author(self, author_id: int) -> Author:
        query = select(Author).where(Author.id == author_id)
        result = await self.session.execute(query)
        author = result.scalar_one_or_none()

        if author is None:
            raise NotFoundException(f'Автор с id {author_id} не найден')
        
        return author
    
    async def create_author(self, author_data: AuthorCreate) -> Author:
        author = Author(**author_data.model_dump())
        self.session.add(author)
        await self.session.commit()
        await self.session.refresh(author)
        return author
    
    async def update_author(self, author_id: int, author_data: AuthorUpdate) -> Author:
        author = await self.get_author(author_id)

        update_data = author_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(author, field, value)

        await self.session.commit()
        await self.session.refresh(author)
        return author
    
    async def delete_author(self, author_id: int) -> None:
        author = await self.get_author(author_id)
        await self.session.delete(author)
        await self.session.commit()