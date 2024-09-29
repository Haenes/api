"""Remove description from project

Revision ID: 9673fb3c1bb3
Revises: 9d5416318f05
Create Date: 2024-09-29 09:08:23.106640+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9673fb3c1bb3'
down_revision: Union[str, None] = '9d5416318f05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
