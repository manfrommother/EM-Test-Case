import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import authors, books, borrows

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(authors.router, prefix=settings.API_V1_STR, tags=["authors"])
app.include_router(books.router, prefix=settings.API_V1_STR, tags=["books"])
app.include_router(borrows.router, prefix=settings.API_V1_STR, tags=["borrows"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {
        "message": "Welcome to Library API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)