"""add product snapshot fields to non_conformities

Revision ID: b4f2d7a9c601
Revises: a7d3c9e41b2f
Create Date: 2026-03-06 12:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4f2d7a9c601'
down_revision = 'a7d3c9e41b2f'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name'] for col in inspector.get_columns('non_conformities')}

    if 'product_code' not in columns:
        op.add_column(
            'non_conformities',
            sa.Column('product_code', sa.String(length=64), nullable=True),
        )

    if 'branch_total_units' not in columns:
        op.add_column(
            'non_conformities',
            sa.Column('branch_total_units', sa.Float(), nullable=True),
        )

    if 'branch_total_usd' not in columns:
        op.add_column(
            'non_conformities',
            sa.Column('branch_total_usd', sa.Float(), nullable=True),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name'] for col in inspector.get_columns('non_conformities')}

    if 'branch_total_usd' in columns:
        op.drop_column('non_conformities', 'branch_total_usd')

    if 'branch_total_units' in columns:
        op.drop_column('non_conformities', 'branch_total_units')

    if 'product_code' in columns:
        op.drop_column('non_conformities', 'product_code')
