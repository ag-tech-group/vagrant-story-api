"""rename blade names from french to english

Revision ID: d5f249b2dc57
Revises: 5cfa7076d3f0
Create Date: 2026-03-20 18:24:13.274586

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5f249b2dc57"
down_revision: str | Sequence[str] | None = "5cfa7076d3f0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (id, old_french_name, new_english_name, old_field_name, new_field_name)
NAME_UPDATES = [
    (1, "Dagger", "Battle Knife", "Battle_Knife", "Battle_Knife"),
    (2, "Stabber", "Scramasax", "Scramasax", "Scramasax"),
    (3, "Combat King", "Dirk", "Dirk", "Dirk"),
    (6, "Dague cannelée", "Cinquedea", "Cinquedea", "Cinquedea"),
    (7, "Suméria", "Kris", "Kris", "Kris"),
    (9, "Kukuri", "Khukuri", "Khukuri", "Khukuri"),
    (10, "Vicelard", "Baselard", "Baselard", "Baselard"),
    (12, "Kubléa", "Jamadhar", "Jamadhar", "Jamadhar"),
    (13, "Brutal", "Spatha", "Spatha", "Spatha"),
    (14, "Cimeterre", "Scimitar", "Scimitar", "Scimitar"),
    (15, "Rapière", "Rapier", "Rapier", "Rapier"),
    (16, "Duel", "Short Sword", "Short_Sword", "Short_Sword"),
    (19, "Strike", "Falchion", "Falchion", "Falchion"),
    (20, "Lame rivetée", "Shotel", "Shotel", "Shotel"),
    (21, "Kora", "Khora", "Khora", "Khora"),
    (24, "Lame ciselée", "Rhomphaia", "Rhomphaia", "Rhomphaia"),
    (25, "Lame dentelée", "Broad Sword", "Broad_Sword", "Broad_Sword"),
    (26, "Norsk", "Norse Sword", "Norse_Sword", "Norse_Sword"),
    (30, "Bestial", "Schiavona", "Schiavona", "Schiavona"),
    (34, "Vent Mortel", "Holy Win", "Holy_Win", "Holy_Win"),
    (35, "Teutonique", "Hand Axe", "Hand_Axe", "Hand_Axe"),
    (36, "Steel Axe", "Battle Axe", "Battle_Axe", "Battle_Axe"),
    (37, "Barbarian", "Francisca", "Francisca", "Francisca"),
    (38, "Tabarzine", "Tabarzin", "Tabarzin", "Tabarzin"),
    (39, "Harvest", "Chamkaq", "Chamkaq", "Chamkaq"),
    (40, "Bardiche", "Tabar", "Tabar", "Tabar"),
    (41, "Abject", "Bullova", "Bullova", "Bullova"),
    (43, "Fléau", "Goblin Club", "Goblin_Club", "Goblin_Club"),
    (44, "Burin", "Spiked Club", "Spiked_Club", "Spiked_Club"),
    (45, "Osselet", "Ball Mace", "Ball_Mace", "Ball_Mace"),
    (46, "Spike Mace", "Footman's Mace", "Spike_Mace", "Footmans_Mace"),
    (49, "Heurtoir", "Bec de Corbin", "Bec_de_Corbin", "Bec_de_Corbin"),
    (50, "Maillet", "War Maul", "War_Maul", "War_Maul"),
    (51, "Narrow Axe", "Guisarme", "Guisarme", "Guisarme"),
    (53, "Corinthien", "Sabre Halberd", "Sabre_Halberd", "Sabre_Halberd"),
    (54, "Terror", "Balbriggan", "Balbriggan", "Balbriggan"),
    (57, "Wizard", "Wizard Staff", "Wizard_Staff", "Wizard_Staff"),
    (58, "Clergy", "Clergy Rod", "Clergy_Rod", "Clergy_Rod"),
    (59, "Diamond", "Summoner Baton", "Summoner_Baton", "Summoner_Baton"),
    (60, "Shamanic", "Shamanic Staff", "Shamanic_Staff", "Shamanic_Staff"),
    (61, "Bishop Cross", "Bishop's Crosier", "Bishops_Crosier", "Bishops_Crosier"),
    (62, "Sagesse", "Sage's Cane", "Sages_Cane", "Sages_Cane"),
    (63, "Mandrin", "Langdebeve", "Langdebeve", "Langdebeve"),
    (65, "Spike Maul", "Footman's Mace", "Spike_Maul", "Footmans_Mace_Heavy"),
    (70, "Hand of Light", "Hand of Light", "Hand_Of_Light", "Hand_of_Light"),
    (71, "Fourche", "Spear", "Spear", "Spear"),
    (72, "Butcher", "Glaive", "Glaive", "Glaive"),
    (73, "Skorpio", "Scorpion", "Scorpion", "Scorpion"),
    (76, "Pike", "Awl Pike", "Awl_Pike", "Awl_Pike"),
    (77, "Lance de chasse", "Boar Spear", "Boar_Spear", "Boar_Spear"),
    (78, "Faucheur", "Fauchard", "Fauchard", "Fauchard"),
    (83, "Power Balist", "Gastraph Bow", "Gastraph_Bow", "Gastraph_Bow"),
    (85, "Arbalestrum", "Target Bow", "Target_Bow", "Target_Bow"),
    (86, "Firebalest", "Windlass", "Windlass", "Windlass"),
    (87, "Crennequin", "Cranequin", "Cranequin", "Cranequin"),
    (90, "Arbrier", "Arbalest", "Arbalest", "Arbalest"),
]


def upgrade() -> None:
    for blade_id, _old_name, new_name, _old_field, new_field in NAME_UPDATES:
        safe_name = new_name.replace("'", "''")
        op.execute(
            f"UPDATE blades SET name = '{safe_name}', field_name = '{new_field}' WHERE id = {blade_id}"
        )


def downgrade() -> None:
    for blade_id, old_name, _new_name, old_field, _new_field in NAME_UPDATES:
        safe_name = old_name.replace("'", "''")
        op.execute(
            f"UPDATE blades SET name = '{safe_name}', field_name = '{old_field}' WHERE id = {blade_id}"
        )
