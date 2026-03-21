from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.character import Character
from app.schemas.game_data import CharacterRead

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("", response_model=list[CharacterRead])
async def list_characters(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Character)
    if q:
        stmt = stmt.where(Character.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Character.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{character_id}", response_model=CharacterRead)
async def get_character(character_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
