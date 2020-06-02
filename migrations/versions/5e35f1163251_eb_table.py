"""eb table

Revision ID: 5e35f1163251
Revises: 8c5c7ab95651
Create Date: 2020-05-27 15:02:27.686433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e35f1163251'
down_revision = '8c5c7ab95651'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('extradition_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('book_name', sa.String(length=70), nullable=True),
    sa.Column('book_author', sa.String(length=100), nullable=True),
    sa.Column('book_date_publ', sa.String(length=5), nullable=True),
    sa.Column('reader_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reader_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extradition_book_timestamp'), 'extradition_book', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_extradition_book_timestamp'), table_name='extradition_book')
    op.drop_table('extradition_book')
    # ### end Alembic commands ###