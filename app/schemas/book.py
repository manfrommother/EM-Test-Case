from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    description: str | None = None
    available_copies: int
    author_id: int


class BookCreate(BookBase):
    pass 


class BookUpdate(BookBase):
    title: str | None = None
    description: str | None = None
    available_copies: int | None = None
    author_id: int | None = None


class BookInDB(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Book(BookInDB):
    pass 