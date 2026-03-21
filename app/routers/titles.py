from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.title import Title
from app.schemas.game_data import TitleRead

router = APIRouter(prefix="/titles", tags=["titles"])


@router.get("", response_model=list[TitleRead])
async def list_titles(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Title)
    if q:
        stmt = stmt.where(Title.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Title.number).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{title_id}", response_model=TitleRead)
async def get_title(title_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Title).where(Title.id == title_id))
    title = result.scalar_one_or_none()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title
