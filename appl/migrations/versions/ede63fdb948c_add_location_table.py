"""add Location  table

Revision ID: ede63fdb948c
Revises: 0b0a51e78618
Create Date: 2023-02-06 10:22:50.941871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ede63fdb948c'
down_revision = '0b0a51e78618'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('city', sa.String(length=60), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('city')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'location', ['city'], ['city'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('location')
    # ### end Alembic commands ###
