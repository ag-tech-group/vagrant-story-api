from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.battle_ability import BattleAbility
from app.schemas.game_data import BattleAbilityRead

router = APIRouter(prefix="/battle-abilities", tags=["battle-abilities"])


@router.get("", response_model=list[BattleAbilityRead])
async def list_battle_abilities(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    q: str | None = None,
    ability_type: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(BattleAbility)
    if q:
        stmt = stmt.where(BattleAbility.name.ilike(f"%{q}%"))
    if ability_type:
        stmt = stmt.where(BattleAbility.ability_type == ability_type)
    stmt = stmt.order_by(BattleAbility.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{ability_id}", response_model=BattleAbilityRead)
async def get_battle_ability(ability_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(BattleAbility).where(BattleAbility.id == ability_id))
    ability = result.scalar_one_or_none()
    if not ability:
        raise HTTPException(status_code=404, detail="Battle Ability not found")
    return ability
