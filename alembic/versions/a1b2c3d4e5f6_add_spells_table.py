"""add spells table

Revision ID: a1b2c3d4e5f6
Revises: b73583770546
Create Date: 2026-03-20 01:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "b73583770546"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SPELLS = [
    # Warlock (ATT) spells
    (
        "Solid Shock",
        "Warlock",
        "25",
        "Singular",
        "Physical",
        "Strikes enemies with an explosive shockwave.",
        "Zephyr",
    ),
    (
        "Lightning Bolt",
        "Warlock",
        "25",
        "Singular",
        "Air",
        "Shoots out arrows of lightning.",
        "Teslae",
    ),
    (
        "Fireball",
        "Warlock",
        "25",
        "Singular",
        "Fire",
        "Pummels enemies with balls of fire.",
        "Incendie",
    ),
    (
        "Vulcan Lance",
        "Warlock",
        "25",
        "Singular",
        "Earth",
        "Showers enemies with volcanic debris.",
        "Terre",
    ),
    (
        "Aqua Blast",
        "Warlock",
        "25",
        "Singular",
        "Water",
        "Engulfs enemies with freezing water blast.",
        "Glace",
    ),
    (
        "Spirit Surge",
        "Warlock",
        "28",
        "Singular",
        "Light",
        "Summons a spirit of light to attack enemies.",
        "Lux",
    ),
    (
        "Dark Chant",
        "Warlock",
        "28",
        "Singular",
        "Dark",
        "Afflicts enemies with crippling pain.",
        "Patir",
    ),
    ("Banish", "Warlock", "25", "Singular", "Dark", "Instant death spell.", "Banish"),
    (
        "Exorcism",
        "Warlock",
        "22",
        "Multiple, cylindrical",
        "Light",
        "Exorcise undead foes.",
        "Exsorcer",
    ),
    (
        "Explosion",
        "Warlock",
        "36, +8 each",
        "Multiple, spherical",
        "Physical",
        "A highly focused, devastating blast.",
        "Demolir",
    ),
    (
        "Thunderburst",
        "Warlock",
        "36, +8 each",
        "Multiple, spherical",
        "Air",
        "Calls down a great bolt from the heavens.",
        "Foudre",
    ),
    (
        "Flame Sphere",
        "Warlock",
        "36, +8 each",
        "Multiple, spherical",
        "Fire",
        "Wreaths target in flames.",
        "Flamme",
    ),
    (
        "Gaea Strike",
        "Warlock",
        "36, +8 each",
        "Multiple, cylindrical",
        "Earth",
        "Creates crushing gravity warp around target.",
        "Gaea",
    ),
    (
        "Avalanche",
        "Warlock",
        "36, +8 each",
        "Multiple, spherical",
        "Water",
        "Super-freezes air around target.",
        "Avalanche",
    ),
    (
        "Radial Surge",
        "Warlock",
        "36, +8 each",
        "Multiple, spherical",
        "Light",
        "Pierces enemies with focused rays of light.",
        "Radius",
    ),
    (
        "Meteor",
        "Warlock",
        "36, +8 each",
        "Multiple, spherical",
        "Dark",
        "Rains meteors down on the target.",
        "Meteore",
    ),
    ("Drain Heart", "Warlock", "12", "Singular", "Dark", "Steals HP from enemies.", "Egout"),
    ("Drain Mind", "Warlock", "2", "Singular", "Dark", "Steals MP from enemies.", "Demance"),
    # Shaman (REC) spells
    ("Heal", "Shaman", "5", "Singular", "Light", "Restores target's HP.", "Guerir"),
    ("Restoration", "Shaman", "3", "Singular", "Light", "Cures Paralysis.", "Mollesse"),
    ("Antidote", "Shaman", "3", "Singular", "Light", "Cures Poison.", "Antidote"),
    ("Blessing", "Shaman", "17", "Singular", "Light", "Cures Curse.", "Benir"),
    (
        "Clearance",
        "Shaman",
        "15",
        "Singular",
        "Light",
        "Cures all status abnormalities.",
        "Purifier",
    ),
    (
        "Surging Balm",
        "Shaman",
        "20",
        "Singular",
        "Light",
        "Recharges HP over a short period of time.",
        "Vie",
    ),
    # Sorcerer (AID) spells
    (
        "Herakles",
        "Sorcerer",
        "12",
        "Singular",
        "None",
        "Temporarily increases target's strength.",
        "Intensite",
    ),
    (
        "Degenerate",
        "Sorcerer",
        "7",
        "Singular",
        "None",
        "Temporarily decreases target's strength.",
        "Debile",
    ),
    (
        "Enlighten",
        "Sorcerer",
        "12",
        "Singular",
        "None",
        "Temporarily increases target's intelligence.",
        "Eclairer",
    ),
    (
        "Psychodrain",
        "Sorcerer",
        "7",
        "Singular",
        "None",
        "Temporarily decreases target's intelligence.",
        "Naugeux",
    ),
    (
        "Invigorate",
        "Sorcerer",
        "12",
        "Singular",
        "None",
        "Temporarily increases target's agility.",
        "Agilite",
    ),
    (
        "Leadbones",
        "Sorcerer",
        "7",
        "Singular",
        "None",
        "Temporarily decreases target's agility.",
        "Tardif",
    ),
    (
        "Prostasia",
        "Sorcerer",
        "15",
        "Singular",
        "None",
        "Temporarily strengthens target's equipment.",
        "Ameliorer",
    ),
    (
        "Tarnish",
        "Sorcerer",
        "7",
        "Singular",
        "None",
        "Temporarily weakens target's equipment.",
        "Deteriorer",
    ),
    (
        "Silence",
        "Sorcerer",
        "7",
        "Singular",
        "None",
        "Temporarily prevents target from casting spells.",
        "Muet",
    ),
    (
        "Magic Ward",
        "Sorcerer",
        "21",
        "Singular",
        "None",
        "Nullifies the next spell cast on target.",
        "Annuler",
    ),
    ("Stun Cloud", "Sorcerer", "7", "Singular", "None", "Paralyzes target.", "Paralysie"),
    ("Poison Mist", "Sorcerer", "11", "Singular", "None", "Poisons target.", "Venin"),
    (
        "Curse",
        "Sorcerer",
        "17",
        "Singular",
        "None",
        "Curses target, lowering their stats.",
        "Fleau",
    ),
    ("Fixate", "Sorcerer", "3", "Cloudstones", "None", "Freezes cloudstones in place.", "Halte"),
    (
        "Dispel",
        "Sorcerer",
        "10",
        "Singular",
        "None",
        "Nullifies any spell currently affecting target.",
        "Dissiper",
    ),
    (
        "Unlock",
        "Sorcerer",
        "3",
        "Treasure chest",
        "None",
        "Opens treasure chests bound with magic.",
        "Clef",
    ),
    (
        "Eureka",
        "Sorcerer",
        "6",
        "Multiple traps",
        "None",
        "Marks all traps in the room.",
        "Visible",
    ),
    (
        "Analyze",
        "Sorcerer",
        "5",
        "Singular",
        "None",
        "Analyzes enemies' parameters and stats.",
        "Analyse",
    ),
    # Enchanter (AFF) spells
    (
        "Luft Fusion",
        "Enchanter",
        "10",
        "Singular",
        "Air",
        "Temporarily strengthens weapon's air affinity.",
        "Sylphe",
    ),
    (
        "Spark Fusion",
        "Enchanter",
        "10",
        "Singular",
        "Fire",
        "Temporarily strengthens weapon's fire affinity.",
        "Salamandre",
    ),
    (
        "Soil Fusion",
        "Enchanter",
        "10",
        "Singular",
        "Earth",
        "Temporarily strengthens weapon's earth affinity.",
        "Gnome",
    ),
    (
        "Frost Fusion",
        "Enchanter",
        "10",
        "Singular",
        "Water",
        "Temporarily strengthens weapon's water affinity.",
        "Undine",
    ),
    (
        "Aero Guard",
        "Enchanter",
        "9",
        "Singular",
        "Air",
        "Temporarily strengthens armor's air affinity.",
        "Parebrise",
    ),
    (
        "Pyro Guard",
        "Enchanter",
        "9",
        "Singular",
        "Fire",
        "Temporarily strengthens armor's fire affinity.",
        "Ignifuge",
    ),
    (
        "Terra Guard",
        "Enchanter",
        "9",
        "Singular",
        "Earth",
        "Temporarily strengthens armor's earth affinity.",
        "Rempart",
    ),
    (
        "Aqua Guard",
        "Enchanter",
        "9",
        "Singular",
        "Water",
        "Temporarily strengthens armor's water affinity.",
        "Barrer",
    ),
    # Teleportation
    (
        "Teleportation",
        "Teleportation",
        "15+",
        "Magic Circle",
        "None",
        "Teleport between save points. Base cost 15 MP, +4 per circle.",
        "",
    ),
]


def upgrade() -> None:
    """Create spells table and populate with data."""
    op.create_table(
        "spells",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("mp_cost", sa.String(length=50), server_default="", nullable=False),
        sa.Column("targeting", sa.String(length=100), server_default="", nullable=False),
        sa.Column("affinity", sa.String(length=50), server_default="", nullable=False),
        sa.Column("effect", sa.Text(), server_default="", nullable=False),
        sa.Column("grimoire", sa.String(length=100), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, category, mp_cost, targeting, affinity, effect, grimoire in SPELLS:
        safe_name = name.replace("'", "''")
        safe_effect = effect.replace("'", "''")
        safe_grimoire = grimoire.replace("'", "''")
        op.execute(
            f"INSERT INTO spells (name, category, mp_cost, targeting, affinity, effect, grimoire) "
            f"VALUES ('{safe_name}', '{category}', '{mp_cost}', '{targeting}', "
            f"'{affinity}', '{safe_effect}', '{safe_grimoire}')"
        )


def downgrade() -> None:
    """Drop spells table."""
    op.drop_table("spells")
