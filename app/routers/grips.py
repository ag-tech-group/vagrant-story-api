from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.grip import Grip
from app.schemas.game_data import GripRead

router = APIRouter(prefix="/grips", tags=["grips"])


@router.get("", response_model=list[GripRead])
async def list_grips(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Grip)
    if q:
        stmt = stmt.where(Grip.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Grip.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{grip_id}", response_model=GripRead)
async def get_grip(grip_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Grip).where(Grip.id == grip_id))
    grip = result.scalar_one_or_none()
    if not grip:
        raise HTTPException(status_code=404, detail="Grip not found")
    return grip
