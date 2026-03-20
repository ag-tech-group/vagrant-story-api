"""enrich consumables with detailed data

Revision ID: f6a7b8c9d0e1
Revises: b73583770546
Create Date: 2026-03-20 06:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f6a7b8c9d0e1"
down_revision: str | Sequence[str] | None = "b73583770546"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (field_name, hp, mp, risk, status_cure, permanent_stat, drop_rate, drop_location)
UPDATES = [
    ("Cure_Root", "50", "", "", "", "", "52/255", "Repent, O ye Sinners and Hallowed Hope"),
    ("Cure_Bulb", "100", "", "", "", "", "", "Numerous, many conditional spawns"),
    ("Cure_Tonic", "150", "", "", "", "", "32/255", "Bonds of Friendship"),
    ("Cure_Potion", "Max", "", "", "", "", "8/255", "Tormentum Insomniae (2nd playthrough)"),
    ("Mana_Root", "", "25", "", "", "", "32/255", "The Squire''s Gathering"),
    ("Mana_Bulb", "", "50", "", "", "", "48/255", "Numerous"),
    ("Mana_Tonic", "", "150", "", "", "", "32/255", "Numerous"),
    ("Mana_Potion", "", "Max", "", "", "", "32/255", "Squassation and Lead Sprinkler"),
    ("Vera_Root", "", "", "25", "", "", "255/255", "Both Stirges, Dreamers'' Entrance"),
    ("Vera_Bulb", "", "", "50", "", "", "32/255", "Numerous"),
    ("Vera_Tonic", "", "", "150", "", "", "32/255", "Hall of Prayer"),
    ("Vera_Potion", "", "", "Max", "", "", "32/255", "Wraith in Parting Regrets"),
    ("Acolytes_Nostrum", "100", "100", "", "", "", "48/255", "Wraith, Sinner''s Sustenence"),
    (
        "Saints_Nostrum",
        "Max",
        "Max",
        "",
        "",
        "",
        "32/255",
        "Skeleton (One Arm) in The Academia Corridor",
    ),
    ("Alchemists_Reagent", "25", "", "25", "", "", "12/255", "Hallway of Heroes"),
    ("Sorcerers_Reagent", "50", "", "50", "", "", "32/255", "Minotaur Lord, Chapel of Meschaunce"),
    (
        "Yggdrasils_Tears",
        "",
        "",
        "",
        "Paralysis",
        "",
        "48/255",
        "Treaty Room and Where Weary Riders Rest",
    ),
    ("Faerie_Chortle", "", "", "", "Poison", "", "255/255", "Numerous incl. Treaty Room"),
    ("Spirit_Orison", "", "", "", "Numbness", "", "48/255", "Where Weary Riders Rest"),
    ("Angelic_Paean", "", "", "", "Curse", "", "64/255", "Harpies (both types)"),
    ("Panacea", "", "", "", "Paralysis, Poison, Numbness", "", "26/255", "Conflict and Accord"),
    ("Snowfly_Draught", "", "", "", "", "", "64/255", "Snowfly Forest"),
    ("Eye_of_Argon", "", "", "", "", "", "64/255", "Underdark Fishmarket"),
    ("Faerie_Wing", "", "", "", "", "", "255/255", "Snowfly Forest, Ichthious"),
    (
        "Elixir_of_Queens",
        "",
        "",
        "",
        "",
        "HP +1-4",
        "48/255",
        "Crusaders in Iron Maiden B2 (2nd playthrough)",
    ),
    ("Elixir_of_Kings", "", "", "", "", "STR +1-4", "16/255", "Undercity West"),
    ("Elixir_of_Sages", "", "", "", "", "INT +1-4", "13/255", "Gharmes Walk"),
    (
        "Elixir_of_Mages",
        "",
        "",
        "",
        "",
        "MP +1-4",
        "38/255",
        "Undercity West or Phantom Dummy (8/255)",
    ),
    ("Elixir_of_Dragoons", "", "", "", "", "AGI +1-4", "8/255", "Dragon Dummy"),
    ("Audentia", "", "", "", "", "HP +1-4", "8/255", "Sanctum, Abandoned Mines B2, Iron Maiden B2"),
    ("Valens", "", "", "", "", "STR +1-4", "8/255", "Abandoned Mines B1, Iron Maiden B2"),
    ("Prudens", "", "", "", "", "INT +1-4", "8/255", "Iron Maiden B2"),
    ("Virtus", "", "", "", "", "MP +1-4", "8/255", "Iron Maiden B2"),
    ("Volare", "", "", "", "", "AGI +1-4", "8/255", "Iron Maiden B2"),
]


def upgrade() -> None:
    """Add enrichment columns to consumables and update data."""
    op.add_column(
        "consumables",
        sa.Column("hp_restore", sa.String(length=50), server_default="", nullable=False),
    )
    op.add_column(
        "consumables",
        sa.Column("mp_restore", sa.String(length=50), server_default="", nullable=False),
    )
    op.add_column(
        "consumables",
        sa.Column("risk_reduce", sa.String(length=50), server_default="", nullable=False),
    )
    op.add_column(
        "consumables",
        sa.Column("status_cure", sa.String(length=100), server_default="", nullable=False),
    )
    op.add_column(
        "consumables",
        sa.Column("permanent_stat", sa.String(length=100), server_default="", nullable=False),
    )
    op.add_column(
        "consumables",
        sa.Column("drop_rate", sa.String(length=100), server_default="", nullable=False),
    )
    op.add_column(
        "consumables",
        sa.Column("drop_location", sa.String(length=300), server_default="", nullable=False),
    )

    for fn, hp, mp, risk, cure, perm, rate, loc in UPDATES:
        sets = []
        if hp:
            sets.append(f"hp_restore = '{hp}'")
        if mp:
            sets.append(f"mp_restore = '{mp}'")
        if risk:
            sets.append(f"risk_reduce = '{risk}'")
        if cure:
            sets.append(f"status_cure = '{cure}'")
        if perm:
            sets.append(f"permanent_stat = '{perm}'")
        if rate:
            sets.append(f"drop_rate = '{rate}'")
        if loc:
            sets.append(f"drop_location = '{loc}'")
        if sets:
            set_clause = ", ".join(sets)
            op.execute(f"UPDATE consumables SET {set_clause} WHERE field_name = '{fn}'")


def downgrade() -> None:
    """Remove enrichment columns from consumables."""
    op.drop_column("consumables", "drop_location")
    op.drop_column("consumables", "drop_rate")
    op.drop_column("consumables", "permanent_stat")
    op.drop_column("consumables", "status_cure")
    op.drop_column("consumables", "risk_reduce")
    op.drop_column("consumables", "mp_restore")
    op.drop_column("consumables", "hp_restore")
