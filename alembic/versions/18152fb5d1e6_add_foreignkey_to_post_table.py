"""add foreignkey to post table

Revision ID: 18152fb5d1e6
Revises: 6a4603657b3b
Create Date: 2025-05-10 15:05:16.747747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18152fb5d1e6'
down_revision: Union[str, None] = '6a4603657b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
