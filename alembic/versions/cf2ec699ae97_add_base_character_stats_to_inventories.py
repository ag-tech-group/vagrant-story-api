"""add base character stats to inventories

Revision ID: cf2ec699ae97
Revises: k5l6m7n8o9p0
Create Date: 2026-03-28 04:25:25.929749

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf2ec699ae97'
down_revision: str | Sequence[str] | None = 'k5l6m7n8o9p0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('inventories', sa.Column('base_hp', sa.Integer(), nullable=True))
    op.add_column('inventories', sa.Column('base_mp', sa.Integer(), nullable=True))
    op.add_column('inventories', sa.Column('base_str', sa.Integer(), nullable=True))
    op.add_column('inventories', sa.Column('base_int', sa.Integer(), nullable=True))
    op.add_column('inventories', sa.Column('base_agi', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('inventories', 'base_agi')
    op.drop_column('inventories', 'base_int')
    op.drop_column('inventories', 'base_str')
    op.drop_column('inventories', 'base_mp')
    op.drop_column('inventories', 'base_hp')
