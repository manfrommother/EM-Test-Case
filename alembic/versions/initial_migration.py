"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-12-11 21:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'initial_migration'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Authors table
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Books table
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('available_copies', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Borrows table
    op.create_table(
        'borrows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reader_name', sa.String(length=200), nullable=False),
        sa.Column('borrow_date', sa.Date(), nullable=False),
        sa.Column('return_date', sa.Date(), nullable=True),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('borrows')
    op.drop_table('books')
    op.drop_table('authors')