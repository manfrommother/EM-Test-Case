from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.author import Author, AuthorCreate, AuthorUpdate
from app.services.author import AuthorService


router = APIRouter(prefix='/authors')


@router.get('', response_model=List[Author])
async def get_authors(
    skip: int=0,
    limit: int=100,
    session: AsyncSession=Depends(get_session)
):
    '''Возвращает список авторов'''
    service = AuthorService(session)
    return await service.get_author(skip=skip, limit=limit)

@router.post('', response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(
        author_data: AuthorCreate,
        session: AsyncSession=Depends(get_session)
):
    '''Создаёт нового автора'''
    service = AuthorService(session)
    return await service.create_author(author_data)

@router.get('/{author_id}', response_model=Author)
async def get_author(
    author_id: int,
    session: AsyncSession=Depends(get_session)
):
    """Возвращает автора по ID"""
    service = AuthorService(session)
    return await service.get_author(author_id)

@router.put('/{author_id}', response_model=Author)
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    session: AsyncSession=Depends(get_session)
):
    '''Обновляет информацию об авторе'''
    service = AuthorService(session)
    return await service.update_author(author_id, author_data)

@router.delete('/{author_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    session: AsyncSession=Depends(get_session)
):
    '''Удаляет автора'''
    service = AuthorService(session)
    await service.delete_author(author_id)