"""add content column to posts table

Revision ID: a9752a0714aa
Revises: 0705779bf1f0
Create Date: 2025-07-30 00:35:58.663231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9752a0714aa'
down_revision: Union[str, Sequence[str], None] = '0705779bf1f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('content', sa.Text(), nullable=True)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
