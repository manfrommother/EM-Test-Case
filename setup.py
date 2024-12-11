from setuptools import setup, find_packages

setup(
    name="library-api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "asyncpg",
        "psycopg2-binary",
    ],
)