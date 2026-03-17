from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.material import Material
from app.schemas.game_data import MaterialRead

router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("", response_model=list[MaterialRead])
async def list_materials(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Material).order_by(Material.tier)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{material_id}", response_model=MaterialRead)
async def get_material(material_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Material).where(Material.id == material_id))
    material = result.scalar_one_or_none()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material
