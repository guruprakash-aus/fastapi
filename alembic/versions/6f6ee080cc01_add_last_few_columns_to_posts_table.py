"""add last few columns to posts table

Revision ID: 6f6ee080cc01
Revises: 4981de12ff39
Create Date: 2025-08-02 20:44:03.596485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f6ee080cc01'
down_revision: Union[str, Sequence[str], None] = '4981de12ff39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=False
        , server_default=sa.func.now()))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), nullable=False
        , server_default=sa.func.now(), onupdate=sa.func.now()))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'updated_at')
    pass
