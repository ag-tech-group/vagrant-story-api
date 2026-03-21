"""add break_arts table

Revision ID: a2b3c4d5e6f7
Revises: d298371e8ad0
Create Date: 2026-03-21 01:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2b3c4d5e6f7"
down_revision: str | Sequence[str] | None = "d298371e8ad0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (name, weapon_type, hp_cost, attack_multiplier, damage_type, affinity, special_effect, kills_required)
BREAK_ARTS = [
    # Dagger
    ("Whistle Sting", "Dagger", 25, "1.1", "Blunt", "As weapon", None, 10),
    ("Shadoweave", "Dagger", 40, "1.2", "Blunt", "Dark", "Paralysis", 65),
    ("Double Fang", "Dagger", 55, "1.2+1.0", "Piercing", "As weapon", "Two hits", 175),
    ("Wyrm Scorn", "Dagger", 75, "1.3", "Piercing", "As weapon", None, 340),
    # Sword
    ("Rending Gale", "Sword", 25, "1.1", "Piercing", "As weapon", None, 20),
    ("Vile Scar", "Sword", 40, "1.2", "Edged", "As weapon", "Poison", 90),
    ("Cherry Ronde", "Sword", 55, "1.2", "Edged", "Water", None, 235),
    ("Papillon Reel", "Sword", 75, "1.3", "Edged", "Light", None, 425),
    # Great Sword
    ("Sunder", "Great Sword", 25, "1.1", "Piercing", "As weapon", None, 25),
    ("Thunderwave", "Great Sword", 40, "1.2", "Edged", "Air", "Paralysis", 110),
    ("Swallow Slash", "Great Sword", 55, "1.2+1.0", "Edged", "As weapon", "Two hits", 260),
    ("Advent Sign", "Great Sword", 75, "1.3", "Edged", "Light", None, 485),
    # Axe/Mace
    ("Mistral Edge", "Axe/Mace", 25, "1.1", "Blunt", "As weapon", None, 18),
    ("Glacial Gale", "Axe/Mace", 40, "1.2", "Blunt", "Air", "Numbness", 80),
    ("Killer Mantis", "Axe/Mace", 55, "1.2+1.5", "Edged", "As weapon", "MP drain (INT)", 210),
    ("Black Nebula", "Axe/Mace", 75, "1.3", "Blunt", "Dark", None, 420),
    # Great Axe
    ("Bear Claw", "Great Axe", 25, "1.1", "Blunt", "As weapon", None, 20),
    ("Accursed Umbra", "Great Axe", 40, "1.2", "Blunt", "As weapon", "Curse", 100),
    ("Iron Ripper", "Great Axe", 55, "1.2", "Blunt", "As weapon", "Damages armor", 245),
    ("Emetic Bomb", "Great Axe", 75, "1.3", "Edged", "As weapon", None, 465),
    # Staff
    ("Sirocco", "Staff", 25, "1.1", "Blunt", "Fire", None, 15),
    ("Riskbreak", "Staff", 40, "1.2", "Piercing", "As weapon", "Cancels RISK", 90),
    ("Gravis Aether", "Staff", 55, "1.2", "Blunt", "Earth", None, 215),
    ("Trinity Pulse", "Staff", 75, "1.3", "Blunt", "As weapon", None, 410),
    # Heavy Mace
    ("Bonecrusher", "Heavy Mace", 25, "1.1", "Blunt", "As weapon", None, 20),
    ("Quickshock", "Heavy Mace", 40, "1.2", "Blunt", "Air", "Numbness", 95),
    ("Ignis Wheel", "Heavy Mace", 55, "1.2+1.0", "Blunt", "As weapon+Fire", "Two hits", 205),
    ("Hex Flux", "Heavy Mace", 75, "1.3+1.0", "Blunt", "Light+Dark", "Two hits", 385),
    # Polearm
    ("Ruination", "Polearm", 25, "1.1", "Piercing", "As weapon", None, 15),
    ("Scythe Wind", "Polearm", 40, "1.2", "Piercing", "Air", "Tarnish", 95),
    ("Giga Tempest", "Polearm", 55, "1.2", "Piercing", "As weapon", "Damages armor", 220),
    ("Spiral Scourge", "Polearm", 75, "1.3", "Piercing", "Water", None, 405),
    # Crossbow
    ("Brimstone Hail", "Crossbow", 25, "1.1+1.0", "Piercing", "Dark+Fire", "Two hits", 20),
    ("Heaven's Scorn", "Crossbow", 40, "1.2+1.0", "Piercing", "Light+Air", "Two hits", 95),
    ("Death Wail", "Crossbow", 55, "1.2+1.0", "Piercing", "Dark+Earth", "Two hits", 230),
    ("Sanctus Flare", "Crossbow", 75, "1.3+1.0", "Piercing", "Light+Water", "Two hits", 430),
    # Bare Hands
    ("Lotus Palm", "Bare Hands", 25, "1.2", "Blunt", "Physical", None, 30),
    ("Vertigo", "Bare Hands", 40, "1.3", "Blunt", "Physical", "Numbness", 105),
    ("Vermillion Aura", "Bare Hands", 55, "1.3+1.0", "Blunt", "Light", "Two hits", 250),
    ("Retribution", "Bare Hands", 75, "1.5", "Blunt", "Dark", None, 460),
]


def upgrade() -> None:
    """Create break_arts table and populate with data."""
    op.create_table(
        "break_arts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("weapon_type", sa.String(length=50), nullable=False),
        sa.Column("hp_cost", sa.Integer(), nullable=False),
        sa.Column("attack_multiplier", sa.String(length=20), nullable=False),
        sa.Column("damage_type", sa.String(length=20), nullable=False),
        sa.Column("affinity", sa.String(length=50), nullable=False),
        sa.Column("special_effect", sa.String(length=100), nullable=True),
        sa.Column("kills_required", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for (
        name,
        weapon_type,
        hp_cost,
        attack_multiplier,
        damage_type,
        affinity,
        special_effect,
        kills_required,
    ) in BREAK_ARTS:
        safe_name = name.replace("'", "''")
        special_sql = f"'{special_effect}'" if special_effect else "NULL"
        op.execute(
            f"INSERT INTO break_arts (name, weapon_type, hp_cost, attack_multiplier, "
            f"damage_type, affinity, special_effect, kills_required) "
            f"VALUES ('{safe_name}', '{weapon_type}', {hp_cost}, '{attack_multiplier}', "
            f"'{damage_type}', '{affinity}', {special_sql}, {kills_required})"
        )


def downgrade() -> None:
    """Drop break_arts table."""
    op.drop_table("break_arts")
