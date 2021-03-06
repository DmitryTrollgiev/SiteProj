"""books table

Revision ID: 8c5c7ab95651
Revises: de5d26260c75
Create Date: 2020-05-22 23:16:38.391411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c5c7ab95651'
down_revision = 'de5d26260c75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_name', sa.String(length=70), nullable=True),
    sa.Column('book_author', sa.String(length=100), nullable=True),
    sa.Column('book_date_publ', sa.String(length=5), nullable=True),
    sa.Column('book_status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    # ### end Alembic commands ###
