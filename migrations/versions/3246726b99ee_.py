"""empty message

Revision ID: 3246726b99ee
Revises: bda454886591
Create Date: 2020-08-29 14:20:10.030823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3246726b99ee'
down_revision = 'bda454886591'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bio', sa.String(length=512), nullable=True))
    op.add_column('user', sa.Column('history', sa.String(length=65536), nullable=True))
    op.add_column('user', sa.Column('rank', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'rank')
    op.drop_column('user', 'history')
    op.drop_column('user', 'bio')
    # ### end Alembic commands ###
