"""add user table

Revision ID: 6a4603657b3b
Revises: 07df5b60dfae
Create Date: 2025-05-09 09:21:25.539741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a4603657b3b'
down_revision: Union[str, None] = '07df5b60dfae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
