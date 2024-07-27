"""Relation fixed

Revision ID: c87a73581b1e
Revises: 4f06d8eb92fd
Create Date: 2024-07-27 09:17:33.834085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c87a73581b1e'
down_revision: Union[str, None] = '4f06d8eb92fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_request', 'users_requests', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_user_request', 'users_requests', ['user_id'])
    # ### end Alembic commands ###
