"""add last few columns to posts table

Revision ID: ae7e7fcad453
Revises: 4f0e3bf35b58
Create Date: 2024-05-30 14:11:33.806599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae7e7fcad453'
down_revision: Union[str, None] = '4f0e3bf35b58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                      nullable=False, server_default=sa.text('now()')))
                    
def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
