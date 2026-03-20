from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.blade import Blade
from app.schemas.game_data import BladeRead

router = APIRouter(prefix="/blades", tags=["blades"])


@router.get("", response_model=list[BladeRead])
async def list_blades(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    blade_type: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Blade)
    if q:
        stmt = stmt.where(Blade.name.ilike(f"%{q}%"))
    if blade_type:
        stmt = stmt.where(Blade.blade_type.ilike(blade_type))
    stmt = stmt.order_by(Blade.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{blade_id}", response_model=BladeRead)
async def get_blade(blade_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Blade).where(Blade.id == blade_id))
    blade = result.scalar_one_or_none()
    if not blade:
        raise HTTPException(status_code=404, detail="Blade not found")
    return blade
