"""fix consumable descriptions from restoration guide

Revision ID: 79e6f0157e5c
Revises: b13f683d0056
Create Date: 2026-03-20 16:07:37.500940

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "79e6f0157e5c"
down_revision: str | Sequence[str] | None = "b13f683d0056"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (field_name, correct_description from restoration.txt / elixirs.txt)
FIXES = [
    ("Mana_Tonic", "Restores 150 MP"),
    ("Vera_Tonic", "Lowers RISK by 150"),
    ("Cure_Potion", "Restores HP to maximum"),
    ("Mana_Potion", "Restores MP to maximum"),
    ("Vera_Potion", "Reduces RISK to zero"),
    ("Saints_Nostrum", "Restores HP and MP to maximum"),
    ("Yggdrasils_Tears", "Removes Paralysis effect"),
    ("Faerie_Chortle", "Removes Poison effect"),
    ("Spirit_Orison", "Removes Numbness effect"),
    ("Angelic_Paean", "Removes Curse effect"),
    ("Panacea", "Removes Paralysis, Poison, and Numbness effects"),
    ("Snowfly_Draught", "Removes magical effects from the target"),
    ("Eye_of_Argon", "Temporarily reveals traps"),
    ("Faerie_Wing", "Temporarily increases Agility and length of jumps"),
    ("Audentia", "Permanently increases HP 1-4"),
    ("Elixir_of_Dragoons", "Permanently increases Agility 1-4"),
    ("Elixir_of_Kings", "Permanently increases Strength 1-4"),
    ("Elixir_of_Mages", "Permanently increases MP 1-4"),
    ("Elixir_of_Queens", "Permanently increases HP 1-4"),
    ("Elixir_of_Sages", "Permanently increases Intelligence 1-4"),
    ("Prudens", "Permanently increases Intelligence 1-4"),
    ("Valens", "Permanently increases Strength 1-4"),
    ("Virtus", "Permanently increases MP 1-4"),
    ("Volare", "Permanently increases Agility 1-4"),
]


def upgrade() -> None:
    for field_name, desc in FIXES:
        escaped = desc.replace("'", "''")
        op.execute(
            f"UPDATE consumables SET description = '{escaped}' WHERE field_name = '{field_name}'"
        )


def downgrade() -> None:
    pass
