"""adding new column called context in post table

Revision ID: 07df5b60dfae
Revises: 1b6a985b67a4
Create Date: 2025-05-09 09:16:17.958727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07df5b60dfae'
down_revision: Union[str, None] = '1b6a985b67a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
