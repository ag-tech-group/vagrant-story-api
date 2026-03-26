from app.routers.areas import router as areas_router
from app.routers.armor import router as armor_router
from app.routers.battle_abilities import router as battle_abilities_router
from app.routers.blades import router as blades_router
from app.routers.break_arts import router as break_arts_router
from app.routers.characters import router as characters_router
from app.routers.chests import router as chests_router
from app.routers.consumables import router as consumables_router
from app.routers.crafting import router as crafting_router
from app.routers.drops import router as drops_router
from app.routers.enemies import router as enemies_router
from app.routers.gems import router as gems_router
from app.routers.grimoires import router as grimoires_router
from app.routers.grips import router as grips_router
from app.routers.keys import router as keys_router
from app.routers.materials import router as materials_router
from app.routers.rankings import router as rankings_router
from app.routers.rooms import router as rooms_router
from app.routers.sigils import router as sigils_router
from app.routers.spells import router as spells_router
from app.routers.titles import router as titles_router
from app.routers.user import router as user_router
from app.routers.workshops import router as workshops_router

__all__ = [
    "areas_router",
    "armor_router",
    "drops_router",
    "battle_abilities_router",
    "blades_router",
    "break_arts_router",
    "characters_router",
    "chests_router",
    "consumables_router",
    "enemies_router",
    "crafting_router",
    "gems_router",
    "grimoires_router",
    "grips_router",
    "keys_router",
    "materials_router",
    "rankings_router",
    "rooms_router",
    "sigils_router",
    "spells_router",
    "titles_router",
    "user_router",
    "workshops_router",
]
