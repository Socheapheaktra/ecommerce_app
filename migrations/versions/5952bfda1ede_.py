"""empty message

Revision ID: 5952bfda1ede
Revises: 6a0eb77fe19a
Create Date: 2023-05-26 09:58:29.245352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5952bfda1ede'
down_revision = '6a0eb77fe19a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('site_user', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('site_user', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)

    # ### end Alembic commands ###
