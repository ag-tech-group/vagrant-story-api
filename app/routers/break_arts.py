from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.break_art import BreakArt
from app.schemas.game_data import BreakArtRead

router = APIRouter(prefix="/break-arts", tags=["break-arts"])


@router.get("", response_model=list[BreakArtRead])
async def list_break_arts(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    q: str | None = None,
    weapon_type: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(BreakArt)
    if q:
        stmt = stmt.where(BreakArt.name.ilike(f"%{q}%"))
    if weapon_type:
        stmt = stmt.where(BreakArt.weapon_type == weapon_type)
    stmt = stmt.order_by(BreakArt.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{break_art_id}", response_model=BreakArtRead)
async def get_break_art(break_art_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(BreakArt).where(BreakArt.id == break_art_id))
    break_art = result.scalar_one_or_none()
    if not break_art:
        raise HTTPException(status_code=404, detail="Break Art not found")
    return break_art
