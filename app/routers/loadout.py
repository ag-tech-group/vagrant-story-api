from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_async_session
from app.models.armor import Armor
from app.models.blade import Blade
from app.models.enemy import Enemy
from app.models.gem import Gem
from app.models.grip import Grip
from app.models.inventory import Inventory, InventoryItem
from app.models.material import Material
from app.rate_limit import limiter
from app.schemas.game_data import (
    LoadoutArmor,
    LoadoutBodyPartScore,
    LoadoutCombinedStats,
    LoadoutEnemyInfo,
    LoadoutRequest,
    LoadoutResponse,
    LoadoutResult,
    LoadoutStats,
    LoadoutWeapon,
)
from app.services.loadout_scorer import optimize_loadout

router = APIRouter(prefix="/loadout", tags=["loadout"])


@router.post("", response_model=LoadoutResponse)
@limiter.limit("10/minute")
async def optimize_loadout_endpoint(
    request: Request,
    body: LoadoutRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Find the best equipment loadout from an inventory to fight a specific enemy."""
    # Validate mode
    if body.mode not in ("full", "offense", "defense"):
        raise HTTPException(status_code=400, detail="Mode must be 'full', 'offense', or 'defense'")

    # Fetch inventory (verify ownership)
    inv_result = await session.execute(
        select(Inventory).where(
            Inventory.id == body.inventory_id,
            Inventory.user_id == user_id,
        )
    )
    inventory = inv_result.scalar_one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    # Fetch enemy with body parts (selectin is the default lazy strategy)
    enemy_result = await session.execute(select(Enemy).where(Enemy.id == body.enemy_id))
    enemy = enemy_result.scalar_one_or_none()
    if not enemy:
        raise HTTPException(status_code=404, detail="Enemy not found")

    # Filter inventory items by storage preferences
    allowed_storage: set[str] = set()
    if body.include_bag:
        allowed_storage.add("bag")
    if body.include_container:
        allowed_storage.add("container")

    filtered_items: list[InventoryItem] = []
    for item in inventory.items:
        if item.storage in allowed_storage:
            # If include_equipped is False, skip items that have an equip_slot
            if not body.include_equipped and item.equip_slot is not None:
                continue
            filtered_items.append(item)

    if not filtered_items:
        return LoadoutResponse(
            enemy=LoadoutEnemyInfo(
                id=enemy.id,
                name=enemy.name,
                enemy_class=enemy.enemy_class,
                hp=enemy.hp,
                mp=enemy.mp,
            ),
            loadouts=[],
        )

    # Fetch all game data needed for scoring
    blades_result = await session.execute(select(Blade))
    blades_db = {b.id: b for b in blades_result.scalars().all()}

    grips_result = await session.execute(select(Grip))
    grips_db = {g.id: g for g in grips_result.scalars().all()}

    armor_result = await session.execute(select(Armor))
    armor_db = {a.id: a for a in armor_result.scalars().all()}

    materials_result = await session.execute(select(Material))
    materials_db = {m.name: m for m in materials_result.scalars().all()}

    gems_result = await session.execute(select(Gem))
    gems_db = {g.id: g for g in gems_result.scalars().all()}

    # Resolve player stats: body overrides > inventory base stats > 0
    player_str = body.player_str if body.player_str is not None else (inventory.base_str or 0)
    player_int = body.player_int if body.player_int is not None else (inventory.base_int or 0)
    player_agi = body.player_agi if body.player_agi is not None else (inventory.base_agi or 0)

    # Run optimizer
    loadouts = optimize_loadout(
        inventory_items=filtered_items,
        enemy=enemy,
        blades_db=blades_db,
        grips_db=grips_db,
        armor_db=armor_db,
        materials_db=materials_db,
        gems_db=gems_db,
        mode=body.mode,
        include_2h=body.include_2h,
        player_str=player_str,
        player_int=player_int,
        player_agi=player_agi,
    )

    # Build response
    loadout_results: list[LoadoutResult] = []
    for loadout in loadouts:
        weapon = None
        if loadout.blade:
            weapon = LoadoutWeapon(
                blade_name=loadout.blade.name,
                blade_type=loadout.blade.blade_type,
                grip_name=loadout.grip.name if loadout.grip else None,
                material=loadout.blade_material.name if loadout.blade_material else "",
                damage_type=loadout.blade.damage_type,
                hands=loadout.blade.hands,
            )

        armor_list = None
        if loadout.armor_pieces:
            armor_list = []
            for slot, (armor_item, mat) in loadout.armor_pieces.items():
                armor_list.append(
                    LoadoutArmor(
                        slot=slot,
                        item_name=armor_item.name,
                        armor_type=armor_item.armor_type,
                        material=mat.name,
                    )
                )

        # Compute combined player stats for this loadout
        cs = loadout.compute_combined_stats()
        combined = LoadoutCombinedStats(
            str_stat=cs["str"],
            int_stat=cs["int"],
            agi_stat=cs["agi"],
            range_stat=cs["range"],
            risk=cs["risk"],
            damage_type=cs["damage_type"],
            blunt=cs["blunt"],
            edged=cs["edged"],
            piercing=cs["piercing"],
            human=cs["human"],
            beast=cs["beast"],
            undead=cs["undead"],
            phantom=cs["phantom"],
            dragon=cs["dragon"],
            evil=cs["evil"],
            physical=cs["physical"],
            fire=cs["fire"],
            water=cs["water"],
            wind=cs["wind"],
            earth=cs["earth"],
            light=cs["light"],
            dark=cs["dark"],
        )

        # Build body part breakdown
        bp_list = [
            LoadoutBodyPartScore(
                name=bp.name,
                estimated_damage=round(bp.estimated_damage, 1),
                hit_chance=bp.hit_chance,
                expected_damage=round(bp.expected_damage, 1),
                is_recommended=(bp.name == loadout.target_body_part),
            )
            for bp in loadout.body_part_scores
        ]

        loadout_results.append(
            LoadoutResult(
                rank=loadout.rank,
                score=round(loadout.score, 2),
                offense_score=round(loadout.offense_score, 2) if loadout.offense_score else None,
                defense_score=round(loadout.defense_score, 2) if loadout.defense_score else None,
                weapon=weapon,
                armor=armor_list,
                stats=LoadoutStats(
                    estimated_damage=round(loadout.estimated_damage, 1),
                    hit_chance=loadout.hit_chance,
                    expected_damage=round(loadout.expected_damage, 1),
                    target_body_part=loadout.target_body_part,
                    target_reason=loadout.target_reason,
                ),
                combined_stats=combined,
                body_parts=bp_list,
            )
        )

    return LoadoutResponse(
        enemy=LoadoutEnemyInfo(
            id=enemy.id,
            name=enemy.name,
            enemy_class=enemy.enemy_class,
            hp=enemy.hp,
            mp=enemy.mp,
        ),
        loadouts=loadout_results,
    )
