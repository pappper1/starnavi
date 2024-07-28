"""field is_blocked added

Revision ID: 571daf0cbb37
Revises: 12e9a5379482
Create Date: 2024-07-28 15:11:31.800769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '571daf0cbb37'
down_revision: Union[str, None] = '12e9a5379482'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('is_blocked', sa.Boolean(), nullable=False))
    op.add_column('post', sa.Column('is_blocked', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'is_blocked')
    op.drop_column('comment', 'is_blocked')
    # ### end Alembic commands ###
