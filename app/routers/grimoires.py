from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.grimoire import Grimoire
from app.schemas.game_data import GrimoireAggregated, GrimoireRead

router = APIRouter(prefix="/grimoires", tags=["grimoires"])


@router.get("", response_model=list[GrimoireAggregated])
async def list_grimoires(
    offset: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Grimoire)
    if q:
        stmt = stmt.where(Grimoire.name.ilike(f"%{q}%") | Grimoire.spell_name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Grimoire.name, Grimoire.id)
    result = await session.execute(stmt)
    rows = result.scalars().all()

    # Aggregate rows by grimoire name
    grouped: dict[str, dict] = {}
    for r in rows:
        if r.name not in grouped:
            grouped[r.name] = {
                "id": r.id,
                "name": r.name,
                "spell_name": r.spell_name,
                "areas": [],
                "sources": [],
                "drop_rates": [],
                "repeatable": r.repeatable,
            }
        g = grouped[r.name]
        area_room = f"{r.area} — {r.room}" if r.room else r.area
        g["areas"].append(area_room)
        g["sources"].append(r.source)
        g["drop_rates"].append(r.drop_rate or "Once")

    aggregated = []
    for g in grouped.values():
        g["areas"] = ", ".join(g["areas"])
        g["sources"] = ", ".join(g["sources"])
        g["drop_rates"] = ", ".join(g["drop_rates"])
        aggregated.append(g)

    return aggregated[offset : offset + limit]


@router.get("/{grimoire_id}", response_model=GrimoireRead)
async def get_grimoire(grimoire_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Grimoire).where(Grimoire.id == grimoire_id))
    grimoire = result.scalar_one_or_none()
    if not grimoire:
        raise HTTPException(status_code=404, detail="Grimoire not found")
    return grimoire
