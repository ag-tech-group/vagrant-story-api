from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.spell import Spell
from app.schemas.game_data import SpellRead

router = APIRouter(prefix="/spells", tags=["spells"])


@router.get("", response_model=list[SpellRead])
async def list_spells(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    q: str | None = None,
    category: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Spell)
    if q:
        stmt = stmt.where(Spell.name.ilike(f"%{q}%"))
    if category:
        stmt = stmt.where(Spell.category == category)
    stmt = stmt.order_by(Spell.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{spell_id}", response_model=SpellRead)
async def get_spell(spell_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Spell).where(Spell.id == spell_id))
    spell = result.scalar_one_or_none()
    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")
    return spell
