"""Added Textbooks table

Revision ID: 839bd3ffbbc2
Revises: 
Create Date: 2024-07-26 23:06:47.340672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '839bd3ffbbc2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
