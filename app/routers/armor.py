from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.armor import Armor
from app.schemas.game_data import ArmorRead

router = APIRouter(prefix="/armor", tags=["armor"])


@router.get("", response_model=list[ArmorRead])
async def list_armor(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    armor_type: str | None = Query(None, alias="type"),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Armor)
    if q:
        stmt = stmt.where(Armor.name.ilike(f"%{q}%"))
    if armor_type:
        stmt = stmt.where(Armor.armor_type.ilike(armor_type))
    stmt = stmt.order_by(Armor.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{armor_id}", response_model=ArmorRead)
async def get_armor(armor_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Armor).where(Armor.id == armor_id))
    armor = result.scalar_one_or_none()
    if not armor:
        raise HTTPException(status_code=404, detail="Armor not found")
    return armor
