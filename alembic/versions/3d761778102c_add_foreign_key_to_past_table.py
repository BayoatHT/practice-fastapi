"""add foreign key to past table

Revision ID: 3d761778102c
Revises: cd1f6b6818d6
Create Date: 2023-04-16 08:07:37.302006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d761778102c'
down_revision = 'cd1f6b6818d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table = "posts",referent_table = "users",
                          local_cols=["owner_id"],remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk')
    op.drop_column('posts','owner_id')
    pass
