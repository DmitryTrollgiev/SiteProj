"""ex table

Revision ID: 052856a039be
Revises: eb304169ac9f
Create Date: 2020-06-01 14:24:24.196643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '052856a039be'
down_revision = 'eb304169ac9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('extradition_book', sa.Column('arrear', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('extradition_book', 'arrear')
    # ### end Alembic commands ###
