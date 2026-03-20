from app.routers.armor import router as armor_router
from app.routers.consumables import router as consumables_router
from app.routers.crafting import router as crafting_router
from app.routers.gems import router as gems_router
from app.routers.grips import router as grips_router
from app.routers.keys import router as keys_router
from app.routers.materials import router as materials_router
from app.routers.sigils import router as sigils_router
from app.routers.spells import router as spells_router
from app.routers.weapons import router as weapons_router

__all__ = [
    "armor_router",
    "consumables_router",
    "crafting_router",
    "gems_router",
    "grips_router",
    "keys_router",
    "materials_router",
    "sigils_router",
    "spells_router",
    "weapons_router",
]
