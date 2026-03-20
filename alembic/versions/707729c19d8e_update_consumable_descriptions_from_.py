"""update consumable descriptions from guide

Revision ID: 707729c19d8e
Revises: 9ac08dc739c2
Create Date: 2026-03-19 23:35:14.084139

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "707729c19d8e"
down_revision: str | Sequence[str] | None = "9ac08dc739c2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE consumables SET description = 'Restores 50 HP' WHERE field_name = 'Cure_Root'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 100 HP' WHERE field_name = 'Cure_Bulb'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 150 HP' WHERE field_name = 'Cure_Tonic'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to max HP' WHERE field_name = 'Elixir_of_Queens'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 25 MP' WHERE field_name = 'Mana_Root'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 50 MP' WHERE field_name = 'Mana_Bulb'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 100 MP' WHERE field_name = 'Mana_Tonic'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to STR' WHERE field_name = 'Elixir_of_Kings'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Lowers RISK by 25' WHERE field_name = 'Vera_Root'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Lowers RISK by 50' WHERE field_name = 'Vera_Bulb'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Lowers RISK by 75' WHERE field_name = 'Vera_Tonic'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to INT' WHERE field_name = 'Elixir_of_Sages'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Temporarily increases speed and jump height' WHERE field_name = 'Faerie_Wing'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Curse' WHERE field_name = 'Angelic_Paean'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cancels all magical effects cast on target' WHERE field_name = 'Snowfly_Draught'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 25 HP, lowers RISK by 25' WHERE field_name = 'Alchemists_Reagent'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Paralysis' WHERE field_name = 'Yggdrasils_Tears'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Paralysis, Poison, and Numbness' WHERE field_name = 'Panacea'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 50 HP, lowers RISK by 50' WHERE field_name = 'Sorcerers_Reagent'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Temporarily reveals traps in the room' WHERE field_name = 'Eye_of_Argon'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores all HP' WHERE field_name = 'Cure_Potion'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores all MP' WHERE field_name = 'Mana_Potion'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Clears all RISK' WHERE field_name = 'Vera_Potion'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 100 HP and MP' WHERE field_name = 'Acolytes_Nostrum'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores all HP and MP' WHERE field_name = 'Saints_Nostrum'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Poison' WHERE field_name = 'Faerie_Chortle'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Numbness' WHERE field_name = 'Spirit_Orison'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to max MP' WHERE field_name = 'Elixir_of_Mages'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to AGI' WHERE field_name = 'Elixir_of_Dragoons'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to max HP' WHERE field_name = 'Audentia'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to max MP' WHERE field_name = 'Virtus'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to STR' WHERE field_name = 'Valens'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to INT' WHERE field_name = 'Prudens'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Permanently adds a few points to AGI' WHERE field_name = 'Volare'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
