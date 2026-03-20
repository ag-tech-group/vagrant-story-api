from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.key import Key
from app.schemas.game_data import KeyRead

router = APIRouter(prefix="/keys", tags=["keys"])


@router.get("", response_model=list[KeyRead])
async def list_keys(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Key)
    if q:
        stmt = stmt.where(Key.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Key.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{key_id}", response_model=KeyRead)
async def get_key(key_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Key).where(Key.id == key_id))
    key = result.scalar_one_or_none()
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    return key
