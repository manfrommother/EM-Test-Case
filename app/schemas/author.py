from datetime import date
from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date


class AuthorCreate(AuthorBase):
    pass 


class AuthorUpdate(AuthorBase):
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None


class AuthorInDB(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Author(AuthorInDB):
    pass 