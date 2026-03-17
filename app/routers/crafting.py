from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.crafting_recipe import CraftingRecipe, MaterialRecipe
from app.schemas.game_data import CraftingRecipeRead, MaterialRecipeRead

router = APIRouter(prefix="/crafting-recipes", tags=["crafting"])


@router.get("", response_model=list[CraftingRecipeRead])
async def list_crafting_recipes(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    category: str | None = None,
    item: str | None = Query(None, description="Search by input or result item name"),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(CraftingRecipe)
    if category:
        stmt = stmt.where(CraftingRecipe.category.ilike(category))
    if item:
        pattern = f"%{item}%"
        stmt = stmt.where(
            or_(
                CraftingRecipe.input_1.ilike(pattern),
                CraftingRecipe.input_2.ilike(pattern),
                CraftingRecipe.result.ilike(pattern),
            )
        )
    stmt = stmt.order_by(CraftingRecipe.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/search", response_model=list[CraftingRecipeRead])
async def search_recipes_by_input(
    input_item: str = Query(..., description="Exact item name to find recipes for"),
    session: AsyncSession = Depends(get_async_session),
):
    """Find all recipes that use a specific item as input."""
    stmt = select(CraftingRecipe).where(
        or_(
            CraftingRecipe.input_1 == input_item,
            CraftingRecipe.input_2 == input_item,
        )
    )
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/result", response_model=list[CraftingRecipeRead])
async def search_recipes_by_result(
    result_item: str = Query(..., description="Exact item name to find how to craft"),
    session: AsyncSession = Depends(get_async_session),
):
    """Find all recipes that produce a specific item."""
    stmt = select(CraftingRecipe).where(CraftingRecipe.result == result_item)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/materials", response_model=list[MaterialRecipeRead])
async def list_material_recipes(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    material: str | None = Query(None, description="Filter by result material"),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(MaterialRecipe)
    if material:
        stmt = stmt.where(MaterialRecipe.result_material.ilike(material))
    stmt = stmt.order_by(MaterialRecipe.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()
