from datetime import date 
from pydantic import BaseModel, ConfigDict

class BorrowBase(BaseModel):
    reader_name: str
    book_id: int
    borrow_date: date
    return_date: date | None = None


class BorrowCreate(BaseModel):
    reader_name: str
    book_id: int


class BorrowUpdate(BaseModel):
    return_date: date


class BorrowInDB(BorrowBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Borrow(BorrowInDB):
    pass 
