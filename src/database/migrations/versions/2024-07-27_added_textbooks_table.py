"""Added Textbooks table

Revision ID: 4f06d8eb92fd
Revises: 
Create Date: 2024-07-27 00:30:58.336219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f06d8eb92fd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('textbooks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('tutor_course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tutor_course_id'], ['tutor_courses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tutor_course_id', name='unique_textbook_tutor_course')
    )
    op.create_index(op.f('ix_textbooks_id'), 'textbooks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_textbooks_id'), table_name='textbooks')
    op.drop_table('textbooks')
    # ### end Alembic commands ###