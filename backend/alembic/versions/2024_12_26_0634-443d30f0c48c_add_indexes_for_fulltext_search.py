"""Add indexes for fulltext search.

Revision ID: 443d30f0c48c
Revises: a934654f00e5
Create Date: 2024-12-26 06:34:50.234821+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '443d30f0c48c'
down_revision: Union[str, None] = 'a934654f00e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('issue_fts_idx', 'issue', [sa.text("to_tsvector('english', title || ' ' || description)")], unique=False, postgresql_using='gin')
    op.create_index('project_fts_idx', 'project', [sa.text("to_tsvector('english', name || ' ' || key)")], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('project_fts_idx', table_name='project', postgresql_using='gin')
    op.drop_index('issue_fts_idx', table_name='issue', postgresql_using='gin')
    # ### end Alembic commands ###