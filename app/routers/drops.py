from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.area import Area
from app.models.enemy import Enemy
from app.models.enemy_encounter import EncounterDrop, EnemyEncounter
from app.models.room import Room
from app.schemas.game_data import ItemDropLocationRead

router = APIRouter(prefix="/drops", tags=["drops"])


@router.get("", response_model=list[ItemDropLocationRead])
async def list_drops(
    item: str = Query(..., description="Item name to search for (case-insensitive)"),
    material: str | None = Query(None, description="Optional material filter"),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = (
        select(
            Enemy.name.label("enemy_name"),
            Enemy.id.label("enemy_id"),
            Enemy.enemy_class.label("enemy_class"),
            Area.name.label("area_name"),
            Area.id.label("area_id"),
            Room.name.label("room_name"),
            EncounterDrop.body_part,
            EncounterDrop.item,
            EncounterDrop.material,
            EncounterDrop.drop_chance,
            EncounterDrop.drop_value,
            EncounterDrop.grip,
            EncounterDrop.quantity,
            EnemyEncounter.condition,
        )
        .join(EnemyEncounter, EncounterDrop.encounter_id == EnemyEncounter.id)
        .join(Enemy, EnemyEncounter.enemy_id == Enemy.id)
        .join(Room, EnemyEncounter.room_id == Room.id)
        .join(Area, Room.area_id == Area.id)
        .where(EncounterDrop.item.ilike(f"%{item}%"))
    )

    if material:
        stmt = stmt.where(EncounterDrop.material.ilike(f"%{material}%"))

    stmt = stmt.order_by(EncounterDrop.drop_value.desc())

    result = await session.execute(stmt)
    return result.mappings().all()
