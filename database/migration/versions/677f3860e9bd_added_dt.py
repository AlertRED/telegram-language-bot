"""some message

Revision ID: 677f3860e9bd
Revises: 30354ee48b80
Create Date: 2023-07-23 01:14:13.368970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '677f3860e9bd'
down_revision = '30354ee48b80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('created_datetime', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.add_column('collection', sa.Column('updated_datetime', sa.DateTime(timezone=True), nullable=False))
    op.add_column('folder', sa.Column('created_datetime', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.add_column('folder', sa.Column('updated_datetime', sa.DateTime(timezone=True), nullable=False))
    op.add_column('term', sa.Column('created_datetime', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.add_column('term', sa.Column('updated_datetime', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('term', 'updated_datetime')
    op.drop_column('term', 'created_datetime')
    op.drop_column('folder', 'updated_datetime')
    op.drop_column('folder', 'created_datetime')
    op.drop_column('collection', 'updated_datetime')
    op.drop_column('collection', 'created_datetime')
    # ### end Alembic commands ###