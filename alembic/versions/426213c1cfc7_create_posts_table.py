"""create posts table

Revision ID: 426213c1cfc7
Revises: 
Create Date: 2023-04-16 06:44:40.939440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '426213c1cfc7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create table
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable=False, primary_key = True),sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
