"""fix consumable data from game guide

Revision ID: 9ac08dc739c2
Revises: acf8b1adae8a
Create Date: 2026-03-19 22:55:32.436444

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ac08dc739c2"
down_revision: str | Sequence[str] | None = "acf8b1adae8a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE consumables SET field_name = 'Cure_Tonic', name = 'Cure Tonic', description = 'Restores 150 HP' WHERE field_name = 'Cure_Toadstool'"
    )
    op.execute(
        "UPDATE consumables SET field_name = 'Mana_Tonic', name = 'Mana Tonic', description = 'Restores 150 MP' WHERE field_name = 'Mana_Toadstool'"
    )
    op.execute(
        "UPDATE consumables SET field_name = 'Vera_Tonic', name = 'Vera Tonic', description = 'Lowers RISK by 150' WHERE field_name = 'Vera_Toadstool'"
    )
    op.execute("DELETE FROM consumables WHERE field_name = 'Amanita'")
    op.execute("DELETE FROM consumables WHERE field_name = 'Nectar_of_the_Gods'")
    op.execute("DELETE FROM consumables WHERE field_name = 'Quicksilver'")
    op.execute("DELETE FROM consumables WHERE field_name = 'Soul_Kiss'")
    op.execute("DELETE FROM consumables WHERE field_name = 'Morion_Gem'")
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Cure_Potion', 'Cure Potion', '', 'Restores all HP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Cure_Potion')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Mana_Potion', 'Mana Potion', '', 'Restores all MP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Mana_Potion')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Vera_Potion', 'Vera Potion', '', 'Clears all RISK' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Vera_Potion')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Acolytes_Nostrum', 'Acolyte''s Nostrum', '', 'Restores 100 HP / MP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Acolytes_Nostrum')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Saints_Nostrum', 'Saint''s Nostrum', '', 'Restores all HP / MP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Saints_Nostrum')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Faerie_Chortle', 'Faerie Chortle', '', 'Cures Poison' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Faerie_Chortle')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Spirit_Orison', 'Spirit Orison', '', 'Cures Numbness' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Spirit_Orison')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Elixir_of_Mages', 'Elixir of Mages', '', 'Adds a few points of MP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Elixir_of_Mages')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Elixir_of_Dragoons', 'Elixir of Dragoons', '', 'Adds a few points of Agility' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Elixir_of_Dragoons')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Audentia', 'Audentia', '', 'Adds a few points of HP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Audentia')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Virtus', 'Virtus', '', 'Adds a few points of MP' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Virtus')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Valens', 'Valens', '', 'Adds a few points of Strength' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Valens')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Prudens', 'Prudens', '', 'Adds a few points of Intelligence' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Prudens')"
    )
    op.execute(
        "INSERT INTO consumables (game_id, field_name, name, description_fr, description) SELECT 0, 'Volare', 'Volare', '', 'Adds a few points of Agility' WHERE NOT EXISTS (SELECT 1 FROM consumables WHERE field_name = 'Volare')"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
