import asyncio
import pytest
from datetime import date
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_session
from app.models.models import Author, Book, Borrow

# Test database URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_db():
    await init_db()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: session
    
    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_author(session: AsyncSession) -> Author:
    author = Author(
        first_name="Test",
        last_name="Author",
        birth_date=date(1990, 1, 1)
    )
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return author


@pytest.fixture
async def test_book(session: AsyncSession, test_author: Author) -> Book:
    book = Book(
        title="Test Book",
        description="Test Description",
        available_copies=5,
        author_id=test_author.id
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


@pytest.fixture
async def test_borrow(session: AsyncSession, test_book: Book) -> Borrow:
    borrow = Borrow(
        reader_name="Test Reader",
        book_id=test_book.id,
        borrow_date=date.today()
    )
    session.add(borrow)
    await session.commit()
    await session.refresh(borrow)
    return borrow