from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.workshop import Workshop
from app.schemas.game_data import WorkshopRead

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("", response_model=list[WorkshopRead])
async def list_workshops(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Workshop)
    if q:
        stmt = stmt.where(Workshop.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Workshop.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{workshop_id}", response_model=WorkshopRead)
async def get_workshop(workshop_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Workshop).where(Workshop.id == workshop_id))
    workshop = result.scalar_one_or_none()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop
