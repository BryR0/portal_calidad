"""add provider_name to non_conformities

Revision ID: a7d3c9e41b2f
Revises: fed909aa9cdd
Create Date: 2026-03-06 10:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7d3c9e41b2f'
down_revision = 'fed909aa9cdd'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name'] for col in inspector.get_columns('non_conformities')}

    if 'provider_name' not in columns:
        op.add_column(
            'non_conformities',
            sa.Column('provider_name', sa.String(length=250), nullable=True),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name'] for col in inspector.get_columns('non_conformities')}

    if 'provider_name' in columns:
        op.drop_column('non_conformities', 'provider_name')
