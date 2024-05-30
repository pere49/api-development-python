"""add foreign key to post table

Revision ID: 4f0e3bf35b58
Revises: 739f8b8895b1
Create Date: 2024-05-30 14:03:36.931234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f0e3bf35b58'
down_revision: Union[str, None] = '739f8b8895b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 
                          source_table='posts', referent_table='users', 
                          local_cols=['user_id'], remote_cols=['id'], 
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'user_id')
