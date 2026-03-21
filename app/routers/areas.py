from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.area import Area
from app.schemas.game_data import AreaDetailRead, AreaRead

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get("", response_model=list[AreaRead])
async def list_areas(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Area)
    if q:
        stmt = stmt.where(Area.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Area.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{area_id}", response_model=AreaDetailRead)
async def get_area(area_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Area).where(Area.id == area_id))
    area = result.scalar_one_or_none()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    # Serialize rooms with area_name
    rooms = [
        {"id": r.id, "name": r.name, "area_id": r.area_id, "area_name": area.name}
        for r in area.rooms
    ]
    return {"id": area.id, "name": area.name, "rooms": rooms}
