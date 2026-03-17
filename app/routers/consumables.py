from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.consumable import Consumable
from app.schemas.game_data import ConsumableRead

router = APIRouter(prefix="/consumables", tags=["consumables"])


@router.get("", response_model=list[ConsumableRead])
async def list_consumables(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Consumable)
    if q:
        stmt = stmt.where(Consumable.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Consumable.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{consumable_id}", response_model=ConsumableRead)
async def get_consumable(consumable_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Consumable).where(Consumable.id == consumable_id))
    consumable = result.scalar_one_or_none()
    if not consumable:
        raise HTTPException(status_code=404, detail="Consumable not found")
    return consumable
