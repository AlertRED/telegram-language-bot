"""added userinfo, find definition statistic

Revision ID: 165feca318ad
Revises: 122feefadc11
Create Date: 2023-08-02 08:31:08.481258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '165feca318ad'
down_revision = '122feefadc11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_info', 'language',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_info', 'language',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
