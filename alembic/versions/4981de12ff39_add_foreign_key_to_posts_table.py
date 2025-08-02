"""add foreign key to posts table

Revision ID: 4981de12ff39
Revises: 5b1bdfc067a2
Create Date: 2025-08-02 20:31:38.656205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4981de12ff39'
down_revision: Union[str, Sequence[str], None] = '5b1bdfc067a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_posts_user_id_users',
        source_table='posts',  # Source table
        referent_table='users',  # Referenced table
        local_cols=['user_id'],  # Source column
        remote_cols=['id'],  # Referenced column
        ondelete='CASCADE'  # Action on delete
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_posts_user_id_users', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
