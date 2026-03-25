from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload

from app.database import get_async_session
from app.models.enemy import Enemy
from app.schemas.game_data import EnemyDetailRead, EnemyRead

router = APIRouter(prefix="/enemies", tags=["enemies"])


@router.get("", response_model=list[EnemyRead])
async def list_enemies(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Enemy).options(noload(Enemy.body_parts), noload(Enemy.drops))
    if q:
        stmt = stmt.where(Enemy.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Enemy.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{enemy_id}", response_model=EnemyDetailRead)
async def get_enemy(enemy_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Enemy).where(Enemy.id == enemy_id).options(selectinload(Enemy.drops))
    )
    enemy = result.scalar_one_or_none()
    if not enemy:
        raise HTTPException(status_code=404, detail="Enemy not found")
    return enemy
