"""create posts table

Revision ID: 0705779bf1f0
Revises:
Create Date: 2025-07-30 00:18:26.001300

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0705779bf1f0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
