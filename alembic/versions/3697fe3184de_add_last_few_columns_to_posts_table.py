"""add last few columns to posts table

Revision ID: 3697fe3184de
Revises: 3d761778102c
Create Date: 2023-04-16 08:40:21.693744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3697fe3184de'
down_revision = '3d761778102c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                sa.Column('published',sa.Boolean(), 
                nullable=False, server_default = "TRUE"),)
    op.add_column('posts',
                sa.Column('created_at',sa.TIMESTAMP(timezone=True), 
                nullable=False, server_default = sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
