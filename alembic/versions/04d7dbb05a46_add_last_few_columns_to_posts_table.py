"""add last few columns to posts table

Revision ID: 04d7dbb05a46
Revises: 18152fb5d1e6
Create Date: 2025-05-10 15:11:02.278624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04d7dbb05a46'
down_revision: Union[str, None] = '18152fb5d1e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
