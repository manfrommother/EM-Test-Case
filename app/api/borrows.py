from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.borrow import Borrow, BorrowCreate, BorrowUpdate
from app.services.borrow import BorrowService

router = APIRouter(prefix="/borrows")


@router.get("", response_model=List[Borrow])
async def get_borrows(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """Get list of borrows"""
    service = BorrowService(session)
    return await service.get_borrows(skip=skip, limit=limit)


@router.post("", response_model=Borrow, status_code=status.HTTP_201_CREATED)
async def create_borrow(
    borrow_data: BorrowCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new borrow record"""
    service = BorrowService(session)
    return await service.create_borrow(borrow_data)


@router.get("/{borrow_id}", response_model=Borrow)
async def get_borrow(
    borrow_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get borrow by ID"""
    service = BorrowService(session)
    return await service.get_borrow(borrow_id)


@router.patch("/{borrow_id}/return", response_model=Borrow)
async def return_book(
    borrow_id: int,
    return_data: BorrowUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Return a borrowed book"""
    service = BorrowService(session)
    return await service.return_book(borrow_id, return_data)