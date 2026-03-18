"""fix_consumables_names

Revision ID: 649d98be5148
Revises: d0c8d71a3452
Create Date: 2026-03-18 00:56:43.182058
"""

from collections.abc import Sequence

from alembic import op

revision: str = "649d98be5148"
down_revision: str | Sequence[str] | None = "d0c8d71a3452"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# French field_name → (English field_name, English display name)
NAME_FIXES = {
    "Racine_HP": ("Cure_Root", "Cure Root"),
    "Bulbe_HP": ("Cure_Bulb", "Cure Bulb"),
    "Algue_HP": ("Cure_Toadstool", "Cure Toadstool"),
    "Potion_HP": ("Elixir_of_Queens", "Elixir of Queens"),
    "Racine_MP": ("Mana_Root", "Mana Root"),
    "Bulbe_MP": ("Mana_Bulb", "Mana Bulb"),
    "Algue_MP": ("Mana_Toadstool", "Mana Toadstool"),
    "Potion_MP": ("Elixir_of_Kings", "Elixir of Kings"),
    "Racine_Risk": ("Vera_Root", "Vera Root"),
    "Bulbe_Risk": ("Vera_Bulb", "Vera Bulb"),
    "Algue_Risk": ("Vera_Toadstool", "Vera Toadstool"),
    "Potion_Risk": ("Elixir_of_Sages", "Elixir of Sages"),
    "Liqueur": ("Faerie_Wing", "Faerie Wing"),
    "Fine_dalcool": ("Angelic_Paean", "Angelic Paean"),
    "Eau_de_vie": ("Amanita", "Amanita"),
    "Digestif": ("Snowfly_Draught", "Snowfly Draught"),
    "Esuna": ("Alchemists_Reagent", "Alchemist's Reagent"),
    "Speed": ("Yggdrasils_Tears", "Yggdrasil's Tears"),
    "Nectar_Frc": ("Nectar_of_the_Gods", "Nectar of the Gods"),
    "Nectar_Int": ("Panacea", "Panacea"),
    "Nectar_Agl": ("Quicksilver", "Quicksilver"),
    "Nectar_HP": ("Soul_Kiss", "Soul Kiss"),
    "Nectar_MP": ("Sorcerers_Reagent", "Sorcerer's Reagent"),
    "Cru_Vaillance": ("Eye_of_Argon", "Eye of Argon"),
    "Cru_Prudence": ("Morion_Gem", "Morion Gem"),
    "Manoir_Vif": ("Gold_Key", "Gold Key"),
    "Château_Audace": ("Silver_Key", "Silver Key"),
    "Saint_Virtux": ("Bronze_Key", "Bronze Key"),
    "Oeil_dArgon": ("Iron_Key", "Iron Key"),
}


def _esc(s: str) -> str:
    return s.replace("'", "''")


def upgrade() -> None:
    for old_fn, (new_fn, new_name) in NAME_FIXES.items():
        op.execute(
            f"UPDATE consumables SET field_name = '{_esc(new_fn)}', name = '{_esc(new_name)}' "
            f"WHERE field_name = '{_esc(old_fn)}'"
        )


def downgrade() -> None:
    for old_fn, (new_fn, _new_name) in NAME_FIXES.items():
        op.execute(
            f"UPDATE consumables SET field_name = '{_esc(old_fn)}' "
            f"WHERE field_name = '{_esc(new_fn)}'"
        )
