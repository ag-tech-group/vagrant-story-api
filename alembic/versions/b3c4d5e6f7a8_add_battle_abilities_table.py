"""add battle_abilities table

Revision ID: b3c4d5e6f7a8
Revises: a2b3c4d5e6f7
Create Date: 2026-03-21 01:01:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3c4d5e6f7a8"
down_revision: str | Sequence[str] | None = "a2b3c4d5e6f7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (name, ability_type, risk_cost, effect, power)
BATTLE_ABILITIES = [
    # Chain abilities (14)
    ("Crimson Pain", "Chain", 2, "HP Damage + self-damage", "100% + 30% self"),
    ("Dulling Impact", "Chain", 3, "Silence", "No damage"),
    ("Gain Life", "Chain", 2, "Restore HP (self)", "30% of hit"),
    ("Gain Magic", "Chain", 2, "Restore MP (self)", "30% of hit"),
    ("Heavy Shot", "Chain", 1, "HP Damage", "70% of hit"),
    ("Instill", "Chain", 1, "HP Damage + restore weapon PP", "10% + 100% PP"),
    ("Mind Ache", "Chain", 1, "MP Damage", "20% of MP lost"),
    ("Mind Assault", "Chain", 1, "MP Damage", "30% of hit"),
    ("Numbing Claw", "Chain", 3, "Numbness", "No damage"),
    ("Paralysis Pulse", "Chain", 3, "Paralysis", "No damage"),
    ("Phantom Pain", "Chain", 3, "HP Damage (weapon PP) + consume PP", "Current PP"),
    ("Raging Ache", "Chain", 1, "HP Damage", "10% of HP lost"),
    ("Snake Venom", "Chain", 3, "Poison", "No damage"),
    ("Temper", "Chain", 2, "HP Damage + restore weapon DP", "40% + 200% DP"),
    # Defense abilities (14)
    ("Absorb Damage", "Defense", 4, "Heal from physical damage", "20% of damage"),
    ("Absorb Magic", "Defense", 4, "Heal from magic damage", "20% of damage"),
    ("Aqua Ward", "Defense", 4, "Heal from water damage", "50% of damage"),
    ("Demonscale", "Defense", 4, "Heal from dark damage", "50% of damage"),
    ("Fireproof", "Defense", 4, "Heal from fire damage", "50% of damage"),
    ("Impact Guard", "Defense", 4, "Heal from physical damage", "50% of damage"),
    ("Phantom Shield", "Defense", 6, "Heal from any damage + consume shield PP", "Current PP"),
    ("Reflect Damage", "Defense", 2, "Reflect physical damage", "40% of damage"),
    ("Reflect Magic", "Defense", 2, "Reflect magic damage", "40% of damage"),
    ("Shadow Guard", "Defense", 4, "Heal from light damage", "50% of damage"),
    ("Siphon Soul", "Defense", 6, "Restore MP from spells", "50% of MP used"),
    ("Terra Ward", "Defense", 4, "Heal from earth damage", "50% of damage"),
    ("Ward", "Defense", 1, "Cure Paralysis + Numbness", "No damage"),
    ("Windbreak", "Defense", 4, "Heal from air damage", "50% of damage"),
]


def upgrade() -> None:
    """Create battle_abilities table and populate with data."""
    op.create_table(
        "battle_abilities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("ability_type", sa.String(length=20), nullable=False),
        sa.Column("risk_cost", sa.Integer(), nullable=False),
        sa.Column("effect", sa.String(length=200), nullable=False),
        sa.Column("power", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, ability_type, risk_cost, effect, power in BATTLE_ABILITIES:
        safe_name = name.replace("'", "''")
        safe_effect = effect.replace("'", "''")
        safe_power = power.replace("'", "''")
        op.execute(
            f"INSERT INTO battle_abilities (name, ability_type, risk_cost, effect, power) "
            f"VALUES ('{safe_name}', '{ability_type}', {risk_cost}, "
            f"'{safe_effect}', '{safe_power}')"
        )


def downgrade() -> None:
    """Drop battle_abilities table."""
    op.drop_table("battle_abilities")
