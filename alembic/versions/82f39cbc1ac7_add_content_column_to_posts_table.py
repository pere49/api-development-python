"""add content column to posts table

Revision ID: 82f39cbc1ac7
Revises: d8e3f7a9deef
Create Date: 2024-05-29 19:06:50.431874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82f39cbc1ac7'
down_revision: Union[str, None] = 'd8e3f7a9deef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
