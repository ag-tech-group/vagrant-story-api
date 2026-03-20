from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.grimoire import Grimoire
from app.schemas.game_data import GrimoireRead

router = APIRouter(prefix="/grimoires", tags=["grimoires"])


@router.get("", response_model=list[GrimoireRead])
async def list_grimoires(
    offset: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Grimoire)
    if q:
        stmt = stmt.where(Grimoire.name.ilike(f"%{q}%") | Grimoire.spell_name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Grimoire.name, Grimoire.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{grimoire_id}", response_model=GrimoireRead)
async def get_grimoire(grimoire_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Grimoire).where(Grimoire.id == grimoire_id))
    grimoire = result.scalar_one_or_none()
    if not grimoire:
        raise HTTPException(status_code=404, detail="Grimoire not found")
    return grimoire
