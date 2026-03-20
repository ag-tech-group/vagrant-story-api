"""add grimoires table

Revision ID: d4e5f6a7b8c9
Revises: b73583770546
Create Date: 2026-03-20 04:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d4e5f6a7b8c9"
down_revision: str | Sequence[str] | None = "b73583770546"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Data from grimoires_2.txt - each source is a separate entry
# (name, spell_name, area, room, source, drop_rate, repeatable)
GRIMOIRES = [
    ("Agilite", "Invigorate", "Snowfly Forest", "Forest River", "Chest", "", False),
    ("Ameliorer", "Prostasia", "Sanctum", "Hall of Sacrilege", "Golem", "", False),
    ("Analyse", "Analyze", "Sanctum", "The Cleansing Chantry", "Dragon", "", False),
    ("Annuler", "Magic Ward", "Snowfly Forest", "Hewn from Nature", "Grissom", "", False),
    ("Antidote", "Antidote", "Catacombs", "The Beast''s Domain", "Lizardman", "", False),
    ("Avalanche", "Avalanche", "Great Cathedral B1", "Order and Chaos", "Marid", "", False),
    (
        "Avalanche",
        "Avalanche",
        "Limestone Quarry",
        "Dream of the Holy Land",
        "Water Elemental",
        "",
        False,
    ),
    ("Avalanche", "Avalanche", "Escapeway", "Fear and Loathing", "Marid", "", False),
    (
        "Avalanche",
        "Avalanche",
        "Temple of Kiltia",
        "Hall of Prayer",
        "Water Elemental",
        "8/255",
        True,
    ),
    ("Avalanche", "Avalanche", "Iron Maiden B1", "The Ducking Stool", "Shadow", "8/255", True),
    ("Banish", "Banish", "Undercity East", "Arms Against Invaders", "Harpy", "13/255", True),
    (
        "Barrer",
        "Aqua Guard",
        "Limestone Quarry",
        "Hall of the Wage-Paying",
        "Snow Dragon",
        "",
        False,
    ),
    ("Benir", "Blessing", "Limestone Quarry", "Bonds of Friendship", "Chest", "", False),
    ("Clef", "Unlock", "Town Center West", "Tircolas Flow", "Duane", "", False),
    ("Debile", "Degenerate", "Wine Cellar", "The Gallows", "Minotaur", "", False),
    ("Demance", "Drain Mind", "Abandoned Mines B2", "Dining in Darkness", "Sky Dragon", "", False),
    ("Demolir", "Explosion", "Great Cathedral L1", "Monk''s Leap", "Lich", "", False),
    ("Demolir", "Explosion", "Town Center West", "Tircolas Flow", "Duane", "", False),
    ("Demolir", "Explosion", "Undercity East", "Where Black Waters Ran", "Lich", "8/255", True),
    ("Deteriorer", "Tarnish", "Snowfly Forest", "Hewn from Nature", "Dark Crusader", "", False),
    ("Dissiper", "Dispel", "Undercity West", "The Children''s Hideout", "Chest", "", False),
    ("Eclairer", "Enlighten", "Undercity East", "Gemsword Blackmarket", "Nightstalker", "", False),
    ("Egout", "Drain Heart", "Limestone Quarry", "Stone and Sulfurous Fire", "Chest", "", False),
    ("Exsorcer", "Exorcism", "Iron Maiden B1", "The Cauldron", "Wraith", "", False),
    ("Flamme", "Flame Sphere", "Great Cathedral B1", "Truth and Lies", "Ifrit", "", False),
    ("Flamme", "Flame Sphere", "Abandoned Mines B1", "The Smeltry", "Fire Elemental", "", False),
    ("Flamme", "Flame Sphere", "Escapeway", "Fear and Loathing", "Ifrit", "", False),
    ("Flamme", "Flame Sphere", "Limestone Quarry", "Excavated Hollow", "Chest", "", False),
    ("Flamme", "Flame Sphere", "Iron Maiden B1", "The Judas Cradle", "Shadow", "8/255", True),
    ("Fleau", "Curse", "Limestone Quarry", "Companions in Arms", "Chest", "", False),
    ("Foudre", "Thunderburst", "Great Cathedral L1", "The Flayed Confessional", "Djinn", "", False),
    (
        "Foudre",
        "Thunderburst",
        "Abandoned Mines B2",
        "The Miner''s End",
        "Air Elemental",
        "",
        False,
    ),
    (
        "Foudre",
        "Thunderburst",
        "Temple of Kiltia",
        "Those who Fear the Light",
        "Air Elemental",
        "8/255",
        True,
    ),
    ("Foudre", "Thunderburst", "Iron Maiden B1", "The Branks", "Shadow", "8/255", True),
    ("Gaea", "Gaea Strike", "Great Cathedral L3", "Hopes of the Idealist", "Dao", "", False),
    (
        "Gaea",
        "Gaea Strike",
        "Abandoned Mines B2",
        "Tomb of the Reborn",
        "Earth Elemental",
        "",
        False,
    ),
    ("Gaea", "Gaea Strike", "Iron Maiden B1", "The Wheel", "Shadow", "8/255", True),
    ("Glace", "Aqua Blast", "Sanctum", "Theology Classroom", "Ghost", "8/255", True),
    (
        "Glace",
        "Aqua Blast",
        "Undercity West",
        "Remembering Days of Yore",
        "Zombie Mage",
        "8/255",
        True,
    ),
    ("Glace", "Aqua Blast", "Undercity West", "Corner of Prayers", "Dark Eye", "8/255", True),
    ("Gnome", "Soil Fusion", "Snowfly Forest", "Hewn from Nature", "Grissom", "", False),
    ("Guerir", "Heal", "Wine Cellar", "The Gallows", "Minotaur", "", False),
    ("Halte", "Fixate", "Sanctum", "Alchemists'' Laboratory", "Chest", "", False),
    (
        "Ignifuge",
        "Pyro Guard",
        "Abandoned Mines B1",
        "The Battle''s Beginning",
        "Wyvern",
        "",
        False,
    ),
    ("Incendie", "Fireball", "Catacombs", "Bandits'' Hideout", "Ghost", "8/255", True),
    (
        "Incendie",
        "Fireball",
        "Undercity West",
        "Sewer of Ravenous Rats",
        "Zombie Mage",
        "8/255",
        True,
    ),
    ("Incendie", "Fireball", "Undercity West", "Nameless Dark Oblivion", "Dark Eye", "8/255", True),
    ("Intensite", "Herakles", "Undercity East", "Place of Free Words", "Harpy", "", False),
    ("Lux", "Spirit Surge", "Wine Cellar", "The Hero''s Winehall", "Dullahan", "", False),
    ("Lux", "Spirit Surge", "Iron Maiden B1", "The Cauldron", "Wraith", "8/255", True),
    ("Meteore", "Meteor", "Great Cathedral L2", "What Ails You, Kills You", "Nightmare", "", False),
    ("Meteore", "Meteor", "Undercity West", "Fear of the Fall", "Dark Elemental", "", False),
    ("Meteore", "Meteor", "Undercity East", "Catspaw Blackmarket", "Lich", "8/255", True),
    ("Meteore", "Meteor", "Escapeway", "Buried Alive", "Chest", "", False),
    ("Mollesse", "Restoration", "Abandoned Mines B2", "Hidden Resources", "Chest", "", False),
    ("Muet", "Silence", "Town Center South", "The House Khazabas", "Chest", "", False),
    ("Nuageux", "Psychodrain", "Undercity East", "Weapons Not Allowed", "Chest", "", False),
    ("Paralysie", "Stun Cloud", "Undercity East", "Catspaw Blackmarket", "Chest", "", False),
    ("Parebrise", "Aero Guard", "Snowfly Forest", "Return to the Land", "Earth Dragon", "", False),
    ("Patir", "Dark Chant", "Undercity West", "Sinner''s Corner", "Dark Eye", "8/255", True),
    ("Patir", "Dark Chant", "Iron Maiden B1", "The Cauldron", "Wraith", "8/255", True),
    ("Purifier", "Clearance", "Temple of Kiltia", "Hall of Prayer", "Last Crusader", "", False),
    ("Radius", "Radial Surge", "Great Cathedral L2", "Maelstrom of Malice", "Lich Lord", "", False),
    ("Radius", "Radial Surge", "Undercity East", "Sale of the Sword", "Lich", "13/255", True),
    ("Radius", "Radial Surge", "Undercity East", "Weapons Not Allowed", "Lich", "13/255", True),
    ("Radius", "Radial Surge", "Escapeway", "Buried Alive", "Chest", "", False),
    ("Rempart", "Terra Guard", "Abandoned Mines B1", "Traitor''s Parting", "Ogre", "", False),
    (
        "Salamandre",
        "Spark Fusion",
        "Abandoned Mines B2",
        "Delusions of Happiness",
        "Chest",
        "",
        False,
    ),
    ("Sylphe", "Luft Fusion", "Undercity West", "Underdark Fishmarket", "Giant Crab", "", False),
    ("Tardif", "Leadbones", "Undercity East", "Sale of the Sword", "Chest", "", False),
    ("Terre", "Vulcan Lance", "Catacombs", "The Withered Spring", "Ghost", "8/255", True),
    (
        "Terre",
        "Vulcan Lance",
        "Undercity West",
        "The Washing-Woman''s Way",
        "Zombie Mage",
        "8/255",
        True,
    ),
    (
        "Terre",
        "Vulcan Lance",
        "Undercity West",
        "The Children''s Hideout",
        "Dark Eye",
        "8/255",
        True,
    ),
    ("Teslae", "Lightning Bolt", "Catacombs", "Rodent-Ridden Chamber", "Ghost", "8/255", True),
    (
        "Teslae",
        "Lightning Bolt",
        "Undercity West",
        "Underdark Fishmarket",
        "Zombie Mage",
        "8/255",
        True,
    ),
    ("Teslae", "Lightning Bolt", "Undercity West", "Fear of the Fall", "Dark Eye", "8/255", True),
    ("Undine", "Frost Fusion", "Abandoned Mines B1", "Rust in Peace", "Chest", "", False),
    ("Venin", "Poison Mist", "Iron Maiden B1", "Starvation", "Wraith", "", False),
    ("Vie", "Surging Balm", "Abandoned Mines B2", "Acolyte''s Burial Vault", "Chest", "", False),
    ("Visible", "Eureka", "Abandoned Mines B1", "Miners'' Resting Hall", "Chest", "", False),
    ("Zephyr", "Solid Shock", "Catacombs", "The Lamenting Mother", "Ghost", "8/255", True),
    ("Zephyr", "Solid Shock", "Undercity West", "Corner of Prayers", "Dark Eye", "8/255", True),
    ("Zephyr", "Solid Shock", "Iron Maiden B1", "Starvation", "Wraith", "8/255", True),
]


def upgrade() -> None:
    """Create grimoires table and populate with data."""
    op.create_table(
        "grimoires",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("spell_name", sa.String(length=100), server_default="", nullable=False),
        sa.Column("area", sa.String(length=100), server_default="", nullable=False),
        sa.Column("room", sa.String(length=200), server_default="", nullable=False),
        sa.Column("source", sa.String(length=200), server_default="", nullable=False),
        sa.Column("drop_rate", sa.String(length=50), server_default="", nullable=False),
        sa.Column("repeatable", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, spell_name, area, room, source, drop_rate, repeatable in GRIMOIRES:
        rep = "true" if repeatable else "false"
        op.execute(
            f"INSERT INTO grimoires (name, spell_name, area, room, source, drop_rate, repeatable) "
            f"VALUES ('{name}', '{spell_name}', '{area}', '{room}', "
            f"'{source}', '{drop_rate}', {rep})"
        )


def downgrade() -> None:
    """Drop grimoires table."""
    op.drop_table("grimoires")
