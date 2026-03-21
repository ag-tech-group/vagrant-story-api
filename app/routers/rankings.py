from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.ranking import Ranking
from app.schemas.game_data import RankingRead

router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get("", response_model=list[RankingRead])
async def list_rankings(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Ranking)
    if q:
        stmt = stmt.where(Ranking.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Ranking.level).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{ranking_id}", response_model=RankingRead)
async def get_ranking(ranking_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Ranking).where(Ranking.id == ranking_id))
    ranking = result.scalar_one_or_none()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")
    return ranking
