"""localize accessory names to english

Revision ID: aa9dcf05f69f
Revises: 9be85acfddc4
Create Date: 2026-03-21 14:17:00.383587

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa9dcf05f69f"
down_revision: str | Sequence[str] | None = "9be85acfddc4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (field_name, english_name) — special cases with apostrophes or spelling fixes
SPECIAL_NAMES = [
    ("Tamulis_Tongue", "Tamuli's Tongue"),
    ("Palolos_Ring", "Palolo's Ring"),
    ("Agriass_Balm", "Agrias's Balm"),
    ("Agrippas_Choker", "Agrippa's Choker"),
    ("Diadras_Earring", "Diadra's Earring"),
    ("Edgars_Ring", "Edgar's Ring"),
    ("Lau_Feis_Armlet", "Lau Fei's Armlet"),
    ("Faufnirs_Tear", "Faufnir's Tear"),
    ("Agaless_Chain", "Agales's Chain"),
    ("Balams_Ring", "Balam's Ring"),
    ("Morgans_Nails", "Morgan's Nails"),
    ("Marlenes_Ring", "Marlene's Ring"),
    ("Talian_Ring", "Talian Ring"),
]


def upgrade() -> None:
    # First: bulk update all accessories using field_name → spaces
    op.execute(
        "UPDATE armor SET name = REPLACE(field_name, '_', ' ') WHERE armor_type = 'Accessory'"
    )

    # Then: fix special cases with apostrophes
    for field_name, english_name in SPECIAL_NAMES:
        escaped = english_name.replace("'", "''")
        op.execute(f"UPDATE armor SET name = '{escaped}' WHERE field_name = '{field_name}'")


def downgrade() -> None:
    pass
