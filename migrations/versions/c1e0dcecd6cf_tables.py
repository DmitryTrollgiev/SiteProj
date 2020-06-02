"""tables

Revision ID: c1e0dcecd6cf
Revises: 5e35f1163251
Create Date: 2020-05-30 15:03:59.950848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1e0dcecd6cf'
down_revision = '5e35f1163251'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('extradition_book', sa.Column('exrt_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('extradition_book', 'exrt_date')
    # ### end Alembic commands ###