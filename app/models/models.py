from datetime import date
from sqlalchemy import String, Date, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[date] = mapped_column(Date)

    books: Mapped[list['Book']] = relationship(
        'Book',
        back_populates='author',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'Author(id={self.id}, name={self.first_name} {self.last_name})'
    

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    available_copies: Mapped[int] = mapped_column(Integer, default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    author: Mapped['Author'] = relationship('Author', back_populates='books')
    borrows: Mapped[list['Borrow']] = relationship(
        'Borrow',
        back_populates='book',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Book(id={self.id}, title={self.title})'
    
class Borrow(Base):
    __tablename__ = 'borrows'

    id: Mapped[int] = mapped_column(primary_key=True)
    reader_name: Mapped[str] = mapped_column(String(200))
    borrow_date: Mapped[date] = mapped_column(Date)
    return_date = Mapped[date] = mapped_column(Date, nullable=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))

    book: Mapped['Book'] = relationship('Book', back_populates='borrows')

    def __repr__(self) -> str:
        return f'Borrow(id={self.id}, book_id={self.book_id}, reader={self.reader_name})'
     