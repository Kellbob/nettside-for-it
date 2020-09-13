"""posts table

Revision ID: 260793e20d16
Revises: 763ab5ff9acf
Create Date: 2020-09-12 15:11:44.763175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '260793e20d16'
down_revision = '763ab5ff9acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('book', sa.VARCHAR(length=140), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###