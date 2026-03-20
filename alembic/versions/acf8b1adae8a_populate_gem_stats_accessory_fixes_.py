"""populate gem stats accessory fixes consumable descriptions

Revision ID: acf8b1adae8a
Revises: bdd18c7d04d7
Create Date: 2026-03-19 22:21:07.203516

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "acf8b1adae8a"
down_revision: str | Sequence[str] | None = "bdd18c7d04d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "physical" = 15, "fire" = -3, "water" = -3, "wind" = -3, "earth" = -3, "light" = -3, "dark" = -3, gem_type = \'Both\' WHERE field_name = \'Talos_Feldspear\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = 30, "fire" = -7, "water" = -7, "wind" = -7, "earth" = -7, "light" = -7, "dark" = -7, gem_type = \'Both\' WHERE field_name = \'Titan_Malachite\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, gem_type = \'Both\' WHERE field_name = \'Sylphid_Topaz\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = -5, "fire" = -5, "water" = -5, "wind" = 30, "earth" = -10, "light" = -5, "dark" = -5, gem_type = \'Both\' WHERE field_name = \'Djinn_Amber\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "fire" = 15, "water" = -5, gem_type = \'Both\' WHERE field_name = \'Salamander_Ruby\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = -5, "fire" = 30, "water" = -10, "wind" = -5, "earth" = -5, "light" = -5, "dark" = -5, gem_type = \'Both\' WHERE field_name = \'Ifrit_Carnelian\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "wind" = -5, "earth" = 15, gem_type = \'Both\' WHERE field_name = \'Gnome_Emerald\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = -5, "fire" = -5, "water" = -5, "wind" = -10, "earth" = 30, "light" = -5, "dark" = -5, gem_type = \'Both\' WHERE field_name = \'Dao_Moonstone\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "fire" = -5, "water" = 15, gem_type = \'Both\' WHERE field_name = \'Undine_Jasper\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = -5, "fire" = -10, "water" = 30, "wind" = -5, "earth" = -5, "light" = -5, "dark" = -5, gem_type = \'Both\' WHERE field_name = \'Marid_Aquamarine\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "light" = 15, "dark" = -5, gem_type = \'Both\' WHERE field_name = \'Angel_Pearl\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = -5, "fire" = -5, "water" = -5, "wind" = -5, "earth" = -5, "light" = 30, "dark" = -10, gem_type = \'Both\' WHERE field_name = \'Seraphim_Diamond\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "light" = -5, "dark" = 15, gem_type = \'Both\' WHERE field_name = \'Morlock_Jet\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "physical" = -5, "fire" = -5, "water" = -5, "wind" = -5, "earth" = -5, "light" = -10, "dark" = 30, gem_type = \'Both\' WHERE field_name = \'Berial_Black_Pearl\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "human" = 15, "beast" = -3, "undead" = -3, gem_type = \'Both\' WHERE field_name = \'Haeralis\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "human" = 30, "beast" = -6, "undead" = -6, "phantom" = -3, "dragon" = -3, "evil" = -3, gem_type = \'Both\' WHERE field_name = \'Orlandu\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "beast" = 15, "undead" = -3, "phantom" = -3, gem_type = \'Both\' WHERE field_name = \'Orion\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "human" = -3, "beast" = 30, "undead" = -6, "phantom" = -6, "dragon" = -3, "evil" = -3, gem_type = \'Both\' WHERE field_name = \'Ogmius\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "undead" = 15, "phantom" = -3, "dragon" = -3, gem_type = \'Both\' WHERE field_name = \'Iocus\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "human" = -3, "beast" = -3, "undead" = 30, "phantom" = -6, "dragon" = -6, "evil" = -3, gem_type = \'Both\' WHERE field_name = \'Balvus\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "phantom" = 15, "dragon" = -3, "evil" = -3, gem_type = \'Both\' WHERE field_name = \'Trinity\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "human" = -3, "beast" = -3, "undead" = -3, "phantom" = 30, "dragon" = -6, "evil" = -6, gem_type = \'Both\' WHERE field_name = \'Beowulf\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "human" = -3, "dragon" = 15, "evil" = -3, gem_type = \'Both\' WHERE field_name = \'Dragonite\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "human" = -6, "beast" = -3, "undead" = -3, "phantom" = -3, "dragon" = 30, "evil" = -6, gem_type = \'Both\' WHERE field_name = \'Sigguld\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 4, "agi" = 3, "human" = -3, "beast" = -3, "evil" = 15, gem_type = \'Both\' WHERE field_name = \'Demonia\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 6, "agi" = 3, "human" = -6, "beast" = -6, "undead" = -3, "phantom" = -3, "dragon" = -3, "evil" = 30, gem_type = \'Both\' WHERE field_name = \'Altema\''
    )
    op.execute(
        'UPDATE gems SET "str" = -3, "int" = 12, "physical" = 20, "fire" = -10, "water" = -10, "wind" = 20, "earth" = 20, "light" = -10, "dark" = -10, gem_type = \'Both\' WHERE field_name = \'Polaris\''
    )
    op.execute(
        'UPDATE gems SET "str" = -3, "int" = 12, "physical" = 20, "fire" = 20, "water" = 20, "wind" = -10, "earth" = -10, "light" = -10, "dark" = -10, gem_type = \'Both\' WHERE field_name = \'Basivalin\''
    )
    op.execute(
        'UPDATE gems SET "str" = -3, "int" = 12, "physical" = 20, "fire" = -10, "water" = -10, "wind" = -10, "earth" = -10, "light" = 20, "dark" = 20, gem_type = \'Both\' WHERE field_name = \'Galerian\''
    )
    op.execute(
        'UPDATE gems SET "str" = 1, "int" = 1, "agi" = 1, "human" = 5, "beast" = 5, "undead" = 5, "phantom" = 5, "dragon" = 5, "evil" = 5, "physical" = 5, "fire" = 5, "water" = 5, "wind" = 5, "earth" = 5, "light" = 5, "dark" = 5, gem_type = \'Both\' WHERE field_name = \'Vedivier\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "int" = 3, "agi" = 2, "human" = 10, "beast" = 10, "undead" = 10, "phantom" = 10, "dragon" = 10, "evil" = 10, "physical" = 10, "fire" = 10, "water" = 10, "wind" = 10, "earth" = 10, "light" = 10, "dark" = 10, gem_type = \'Both\' WHERE field_name = \'Berion\''
    )
    op.execute(
        'UPDATE gems SET "str" = 3, "int" = 6, "agi" = 3, "human" = 15, "beast" = 15, "undead" = 15, "phantom" = 15, "dragon" = 15, "evil" = 15, "physical" = 15, "fire" = 15, "water" = 15, "wind" = 15, "earth" = 15, "light" = 15, "dark" = 15, gem_type = \'Both\' WHERE field_name = \'Gervin\''
    )
    op.execute(
        'UPDATE gems SET "str" = 4, "int" = 9, "agi" = 4, "human" = 20, "beast" = 20, "undead" = 20, "phantom" = 20, "dragon" = 20, "evil" = 20, "physical" = 20, "fire" = 20, "water" = 20, "wind" = 20, "earth" = 20, "light" = 20, "dark" = 20, gem_type = \'Both\' WHERE field_name = \'Tertia\''
    )
    op.execute(
        'UPDATE gems SET "str" = 5, "int" = 12, "agi" = 5, "human" = 25, "beast" = 25, "undead" = 25, "phantom" = 25, "dragon" = 25, "evil" = 25, "physical" = 25, "fire" = 25, "water" = 25, "wind" = 25, "earth" = 25, "light" = 25, "dark" = 25, gem_type = \'Both\' WHERE field_name = \'Lancer\''
    )
    op.execute(
        'UPDATE gems SET "str" = 8, "int" = 15, "agi" = 8, "human" = 30, "beast" = 30, "undead" = 30, "phantom" = 30, "dragon" = 30, "evil" = 30, "physical" = 30, "fire" = 30, "water" = 30, "wind" = 30, "earth" = 30, "light" = 30, "dark" = 30, gem_type = \'Both\' WHERE field_name = \'Arturos\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "agi" = 5, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Weapon\', description = \'Adds 20% to the hit rate of all weapon attacks.\' WHERE field_name = \'Braveheart\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "agi" = 5, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Weapon\', description = \'Adds 20% to the hit rate of all magick spells.\' WHERE field_name = \'Hellraiser\''
    )
    op.execute(
        'UPDATE gems SET "str" = 2, "agi" = 8, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces hit rate of attacks targetting Ashley by 20%. This also affects Chain Abilities like Instill or Temper.\' WHERE field_name = \'Nightkiller\''
    )
    op.execute(
        'UPDATE gems SET "int" = 3, "agi" = 5, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces hit rate of magicks targetting Ashley by 20%. This also affects beneficial spells like Heal or the various Fusions.\' WHERE field_name = \'Manabreaker\''
    )
    op.execute(
        'UPDATE gems SET "agi" = 1, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Str-Down succeeding by 20%.\' WHERE field_name = \'Powerfist\''
    )
    op.execute(
        'UPDATE gems SET "agi" = 1, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Int-Down succeeding by 20%.\' WHERE field_name = \'Brainshield\''
    )
    op.execute(
        'UPDATE gems SET "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Agi-Down succeeding by 20%.\' WHERE field_name = \'Speedster\''
    )
    op.execute(
        'UPDATE gems SET "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Silence succeeding by 20%.\' WHERE field_name = \'Silent_Queen\''
    )
    op.execute(
        'UPDATE gems SET "agi" = 1, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Paralysis succeeding by 20%.\' WHERE field_name = \'Dark_Queen\''
    )
    op.execute(
        'UPDATE gems SET "agi" = 1, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Instant Death succeeding by 20%.\' WHERE field_name = \'Death_Queen\''
    )
    op.execute(
        'UPDATE gems SET "agi" = 1, "human" = 3, "beast" = 3, "undead" = 3, "phantom" = 3, "dragon" = 3, "evil" = 3, "physical" = 3, "fire" = 3, "water" = 3, "wind" = 3, "earth" = 3, "light" = 3, "dark" = 3, gem_type = \'Shield\', description = \'Reduces chance of Numbness succeeding by 20%.\' WHERE field_name = \'White_Queen\''
    )
    op.execute(
        'UPDATE armor SET "str" = 0, "int" = 1, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 5, "phantom" = -5, "dragon" = -5, "evil" = 5, "physical" = 5, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 5, "dark" = -5, "blunt" = 0, "edged" = 0, "piercing" = 0 WHERE field_name = \'Rood_Necklace\''
    )
    op.execute(
        'UPDATE armor SET "str" = 0, "int" = 3, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 10, "dragon" = -10, "evil" = 10, "physical" = 0, "fire" = 10, "water" = 10, "wind" = 10, "earth" = 10, "light" = 10, "dark" = 10, "blunt" = 0, "edged" = 0, "piercing" = -10 WHERE field_name = \'Rune_Earrings\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 15, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 0, "edged" = 10, "piercing" = 15 WHERE field_name = \'Lionhead\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 30, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 15, "edged" = 5, "piercing" = 0 WHERE field_name = \'Rusted_Nails\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 15, "earth" = -10, "light" = 0, "dark" = 0, "blunt" = 5, "edged" = 15, "piercing" = 10 WHERE field_name = \'Sylphid_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 30, "earth" = -25, "light" = 0, "dark" = 0, "blunt" = 10, "edged" = 0, "piercing" = 5 WHERE field_name = \'Marduk\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 15, "water" = -10, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 10, "edged" = 0, "piercing" = 5 WHERE field_name = \'Salamander_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 30, "water" = -25, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 5, "edged" = 15, "piercing" = 10 WHERE field_name = \'Tamulis_Tongue\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = -10, "earth" = 15, "light" = 0, "dark" = 0, "blunt" = 0, "edged" = 5, "piercing" = 15 WHERE field_name = \'Gnome_Bracelet\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = -25, "earth" = 30, "light" = 0, "dark" = 0, "blunt" = 15, "edged" = 10, "piercing" = 0 WHERE field_name = \'Palolos_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = -10, "water" = 15, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 5, "edged" = 10, "piercing" = 5 WHERE field_name = \'Undine_Bracelet\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = -25, "water" = 30, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 10, "edged" = 5, "piercing" = 10 WHERE field_name = \'Talian_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 15, "dark" = -10, "blunt" = 0, "edged" = 10, "piercing" = 15 WHERE field_name = \'Agriass_Balm\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 30, "dark" = -25, "blunt" = 15, "edged" = 5, "piercing" = 0 WHERE field_name = \'Kadesh_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = -10, "dark" = 15, "blunt" = 10, "edged" = 0, "piercing" = 10 WHERE field_name = \'Agrippas_Choker\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = -25, "dark" = 30, "blunt" = 5, "edged" = 15, "piercing" = 5 WHERE field_name = \'Diadras_Earring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 15, "beast" = -5, "undead" = -5, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 0, "edged" = 10, "piercing" = 15 WHERE field_name = \'Titans_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 30, "beast" = -12, "undead" = -12, "phantom" = 0, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 15, "edged" = 5, "piercing" = 0 WHERE field_name = \'Lau_Feis_Armlet\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 15, "undead" = -5, "phantom" = -5, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 5, "edged" = 15, "piercing" = 10 WHERE field_name = \'Swan_Song\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 30, "undead" = -12, "phantom" = -12, "dragon" = 0, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 10, "edged" = 0, "piercing" = 5 WHERE field_name = \'Pushpaka\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 15, "phantom" = -5, "dragon" = -5, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 10, "edged" = 0, "piercing" = 5 WHERE field_name = \'Edgars_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 30, "phantom" = -12, "dragon" = -12, "evil" = 0, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 5, "edged" = 15, "piercing" = 10 WHERE field_name = \'Cross_Choker\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 15, "dragon" = -5, "evil" = -5, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 0, "edged" = 5, "piercing" = 15 WHERE field_name = \'Ghost_Hound\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = 0, "beast" = 0, "undead" = 0, "phantom" = 30, "dragon" = -12, "evil" = -12, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 15, "edged" = 10, "piercing" = 0 WHERE field_name = \'Beaded_Amulet\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = -5, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 15, "evil" = -5, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 5, "edged" = 20, "piercing" = 5 WHERE field_name = \'Dragonhead\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = -12, "beast" = 0, "undead" = 0, "phantom" = 0, "dragon" = 30, "evil" = -12, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 10, "edged" = 5, "piercing" = 10 WHERE field_name = \'Faufnirs_Tear\''
    )
    op.execute(
        'UPDATE armor SET "str" = 3, "int" = 3, "agi" = 0, "human" = -5, "beast" = -5, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 15, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 0, "edged" = 10, "piercing" = 0 WHERE field_name = \'Agaless_Chain\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 5, "agi" = 1, "human" = -12, "beast" = -12, "undead" = 0, "phantom" = 0, "dragon" = 0, "evil" = 30, "physical" = 0, "fire" = 0, "water" = 0, "wind" = 0, "earth" = 0, "light" = 0, "dark" = 0, "blunt" = 15, "edged" = 5, "piercing" = 0 WHERE field_name = \'Balams_Ring\''
    )
    op.execute(
        'UPDATE armor SET "str" = 5, "int" = 10, "agi" = 2, "human" = -10, "beast" = 15, "undead" = 25, "phantom" = -15, "dragon" = 25, "evil" = -5, "physical" = -15, "fire" = 25, "water" = 25, "wind" = 25, "earth" = 25, "light" = -5, "dark" = -15, "blunt" = 20, "edged" = -20, "piercing" = -15 WHERE field_name = \'Ninja_Coif\''
    )
    op.execute(
        'UPDATE armor SET "str" = 10, "int" = 15, "agi" = 2, "human" = 15, "beast" = 15, "undead" = 15, "phantom" = 15, "dragon" = 15, "evil" = 15, "physical" = 15, "fire" = 15, "water" = 15, "wind" = 15, "earth" = 15, "light" = 15, "dark" = 15, "blunt" = 15, "edged" = 15, "piercing" = 15 WHERE field_name = \'Morgans_Nails\''
    )
    op.execute(
        'UPDATE armor SET "str" = 20, "int" = 25, "agi" = 5, "human" = 25, "beast" = 25, "undead" = 25, "phantom" = 25, "dragon" = 25, "evil" = 25, "physical" = 25, "fire" = 25, "water" = 25, "wind" = 25, "earth" = 25, "light" = 25, "dark" = 25, "blunt" = 0, "edged" = 0, "piercing" = 0 WHERE field_name = \'Marlenes_Ring\''
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 50 HP' WHERE field_name = 'Cure_Root'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 100 HP' WHERE field_name = 'Cure_Bulb'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Adds a few points of HP' WHERE field_name = 'Elixir_of_Queens'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 25 MP' WHERE field_name = 'Mana_Root'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 50 MP' WHERE field_name = 'Mana_Bulb'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Adds a few points of Strength' WHERE field_name = 'Elixir_of_Kings'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Lowers RISK by 25' WHERE field_name = 'Vera_Root'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Lowers RISK by 50' WHERE field_name = 'Vera_Bulb'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Adds a few points of Intelligence' WHERE field_name = 'Elixir_of_Sages'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Temporarily increases speed and jumps' WHERE field_name = 'Faerie_Wing'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Curse' WHERE field_name = 'Angelic_Paean'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cancels magical effects cast on target' WHERE field_name = 'Snowfly_Draught'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 25 HP / lowers RISK by 25' WHERE field_name = 'Alchemists_Reagent'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Paralysis' WHERE field_name = 'Yggdrasils_Tears'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Cures Paralysis / Poison / Numbness' WHERE field_name = 'Panacea'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Restores 50 HP / lowers RISK by 50' WHERE field_name = 'Sorcerers_Reagent'"
    )
    op.execute(
        "UPDATE consumables SET description = 'Temporarily allows Ashley to see traps' WHERE field_name = 'Eye_of_Argon'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
