"""add user table

Revision ID: cd1f6b6818d6
Revises: a98c485d568a
Create Date: 2023-04-16 07:55:52.056252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd1f6b6818d6'
down_revision = 'a98c485d568a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id',sa.Integer, primary_key = True, nullable = False),
    sa.Column('email',sa.String, nullable = False, unique=True),
    sa.Column('password',sa.String, nullable = False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True), 
              nullable = False, server_default = sa.text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
