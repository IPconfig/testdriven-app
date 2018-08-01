""" Add admin column

Revision ID: 813d176fab9f
Revises: 9c02c1dd706f
Create Date: 2018-08-01 14:14:34.314189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '813d176fab9f'
down_revision = '9c02c1dd706f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    op.execute('UPDATE users SET admin=False')
    op.alter_column('users', 'admin', nullable=False)


def downgrade():
    op.drop_column('users', 'admin')
