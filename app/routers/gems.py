from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.gem import Gem
from app.schemas.game_data import GemRead

router = APIRouter(prefix="/gems", tags=["gems"])


@router.get("", response_model=list[GemRead])
async def list_gems(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Gem)
    if q:
        stmt = stmt.where(Gem.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Gem.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{gem_id}", response_model=GemRead)
async def get_gem(gem_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Gem).where(Gem.id == gem_id))
    gem = result.scalar_one_or_none()
    if not gem:
        raise HTTPException(status_code=404, detail="Gem not found")
    return gem
