"""add content column to posts table

Revision ID: a98c485d568a
Revises: 426213c1cfc7
Create Date: 2023-04-16 07:36:14.352639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a98c485d568a'
down_revision = '426213c1cfc7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('Content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','Content')
    pass
