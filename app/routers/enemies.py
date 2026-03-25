from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload

from app.database import get_async_session
from app.models.enemy import Enemy
from app.models.enemy_encounter import EnemyEncounter
from app.models.room import Room
from app.schemas.game_data import EnemyDetailRead, EnemyEncounterRead, EnemyRead

router = APIRouter(prefix="/enemies", tags=["enemies"])


@router.get("", response_model=list[EnemyRead])
async def list_enemies(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Enemy).options(
        noload(Enemy.body_parts), noload(Enemy.drops), noload(Enemy.encounters)
    )
    if q:
        stmt = stmt.where(Enemy.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Enemy.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{enemy_id}", response_model=EnemyDetailRead)
async def get_enemy(enemy_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Enemy)
        .where(Enemy.id == enemy_id)
        .options(
            selectinload(Enemy.drops),
            selectinload(Enemy.encounters)
            .selectinload(EnemyEncounter.room)
            .selectinload(Room.area),
        )
    )
    enemy = result.scalar_one_or_none()
    if not enemy:
        raise HTTPException(status_code=404, detail="Enemy not found")

    # Build encounter read objects with room/area names and drops
    encounter_reads = []
    for enc in enemy.encounters:
        room = enc.room
        encounter_reads.append(
            EnemyEncounterRead(
                id=enc.id,
                enemy_id=enc.enemy_id,
                room_id=enc.room_id,
                room_name=room.name if room else "",
                area_id=room.area_id if room else 0,
                area_name=room.area.name if room and room.area else "",
                condition=enc.condition,
                attacks=enc.attacks,
                drops=enc.drops,
            )
        )

    # Build response manually to inject encounter reads
    return EnemyDetailRead(
        id=enemy.id,
        name=enemy.name,
        enemy_class=enemy.enemy_class,
        hp=enemy.hp,
        mp=enemy.mp,
        str_stat=enemy.str_stat,
        int_stat=enemy.int_stat,
        agi_stat=enemy.agi_stat,
        encyclopaedia_number=enemy.encyclopaedia_number,
        description=enemy.description,
        movement=enemy.movement,
        is_boss=enemy.is_boss,
        body_parts=enemy.body_parts,
        drops=enemy.drops,
        encounters=encounter_reads,
    )
