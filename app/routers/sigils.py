from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.sigil import Sigil
from app.schemas.game_data import SigilRead

router = APIRouter(prefix="/sigils", tags=["sigils"])


@router.get("", response_model=list[SigilRead])
async def list_sigils(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Sigil)
    if q:
        stmt = stmt.where(Sigil.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Sigil.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{sigil_id}", response_model=SigilRead)
async def get_sigil(sigil_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Sigil).where(Sigil.id == sigil_id))
    sigil = result.scalar_one_or_none()
    if not sigil:
        raise HTTPException(status_code=404, detail="Sigil not found")
    return sigil
