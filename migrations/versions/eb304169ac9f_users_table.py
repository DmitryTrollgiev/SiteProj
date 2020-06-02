"""users table

Revision ID: eb304169ac9f
Revises: c1e0dcecd6cf
Create Date: 2020-06-01 13:23:46.451419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb304169ac9f'
down_revision = 'c1e0dcecd6cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('extradition_book', sa.Column('book_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('extradition_book', 'book_id')
    # ### end Alembic commands ###