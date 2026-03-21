from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.models.room import Room
from app.schemas.game_data import RoomDetailRead, RoomRead

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomRead])
async def list_rooms(
    offset: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    area: int | None = None,
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Room).options(selectinload(Room.area))
    if area:
        stmt = stmt.where(Room.area_id == area)
    if q:
        stmt = stmt.where(Room.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Room.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    rooms = result.scalars().all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "area_id": r.area_id,
            "area_name": r.area.name if r.area else "",
        }
        for r in rooms
    ]


@router.get("/{room_id}", response_model=RoomDetailRead)
async def get_room(room_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Room).options(selectinload(Room.area)).where(Room.id == room_id)
    )
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "id": room.id,
        "name": room.name,
        "area_id": room.area_id,
        "area_name": room.area.name if room.area else "",
    }
