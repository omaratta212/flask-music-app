"""empty message

Revision ID: 8fac82829298
Revises: 745517dc1436
Create Date: 2020-07-16 12:33:04.797815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fac82829298'
down_revision = '745517dc1436'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'seeking_description')
    # ### end Alembic commands ###
