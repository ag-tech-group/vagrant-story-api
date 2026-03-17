from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.weapon import Weapon
from app.schemas.game_data import WeaponRead

router = APIRouter(prefix="/weapons", tags=["weapons"])


@router.get("", response_model=list[WeaponRead])
async def list_weapons(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    blade_type: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Weapon)
    if q:
        stmt = stmt.where(Weapon.name.ilike(f"%{q}%"))
    if blade_type:
        stmt = stmt.where(Weapon.blade_type.ilike(blade_type))
    stmt = stmt.order_by(Weapon.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{weapon_id}", response_model=WeaponRead)
async def get_weapon(weapon_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Weapon).where(Weapon.id == weapon_id))
    weapon = result.scalar_one_or_none()
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon
