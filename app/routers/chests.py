from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload

from app.database import get_async_session
from app.models.chest import Chest
from app.schemas.game_data import ChestListRead, ChestRead

router = APIRouter(prefix="/chests", tags=["chests"])


@router.get("", response_model=list[ChestListRead])
async def list_chests(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    area: str | None = None,
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Chest).options(noload(Chest.items))
    if area:
        stmt = stmt.where(Chest.area.ilike(f"%{area}%"))
    if q:
        stmt = stmt.where(Chest.room.ilike(f"%{q}%"))
    stmt = stmt.order_by(Chest.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{chest_id}", response_model=ChestRead)
async def get_chest(chest_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Chest).where(Chest.id == chest_id))
    chest = result.scalar_one_or_none()
    if not chest:
        raise HTTPException(status_code=404, detail="Chest not found")
    return chest
