from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import authors, books, borrows


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f'{settings.API_V1_STR}/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(authors.router, prefix=settings.API_V1_STR, tags=['authors'])
app.include_router(books.router, prefix=settings.API_V1_STR, tags=['books'])
app.include_router(borrows.router, prefix=settings.API_V1_STR, tags=['borrows'])

@app.get('/')
async def root():
    return{
        "message": "Welcome to Library API",
        "version": settings.VERSION,
        "docs_url": '/docs'
    }