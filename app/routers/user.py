from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_async_session
from app.models.inventory import Inventory, InventoryItem
from app.schemas.game_data import (
    InventoryCreate,
    InventoryItemCreate,
    InventoryItemRead,
    InventoryItemUpdate,
    InventoryListRead,
    InventoryRead,
    InventoryUpdate,
)

router = APIRouter(prefix="/user/inventories", tags=["user"])


async def _get_user_inventory(
    inventory_id: int,
    user_id: str,
    session: AsyncSession,
) -> Inventory:
    """Fetch an inventory and verify it belongs to the current user."""
    result = await session.execute(
        select(Inventory).where(Inventory.id == inventory_id, Inventory.user_id == user_id)
    )
    inventory = result.scalar_one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.get("", response_model=list[InventoryListRead])
async def list_inventories(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Inventory).where(Inventory.user_id == user_id).order_by(Inventory.created_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=InventoryRead, status_code=201)
async def create_inventory(
    body: InventoryCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    inventory = Inventory(user_id=user_id, name=body.name)
    session.add(inventory)
    await session.commit()
    await session.refresh(inventory)
    return inventory


@router.get("/{inventory_id}", response_model=InventoryRead)
async def get_inventory(
    inventory_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await _get_user_inventory(inventory_id, user_id, session)


@router.put("/{inventory_id}", response_model=InventoryRead)
async def update_inventory(
    inventory_id: int,
    body: InventoryUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    inventory = await _get_user_inventory(inventory_id, user_id, session)
    inventory.name = body.name
    await session.commit()
    await session.refresh(inventory)
    return inventory


@router.delete("/{inventory_id}", status_code=204)
async def delete_inventory(
    inventory_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    inventory = await _get_user_inventory(inventory_id, user_id, session)
    await session.delete(inventory)
    await session.commit()


@router.post("/{inventory_id}/items", response_model=InventoryItemRead, status_code=201)
async def add_item(
    inventory_id: int,
    body: InventoryItemCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await _get_user_inventory(inventory_id, user_id, session)
    item = InventoryItem(inventory_id=inventory_id, **body.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.put("/{inventory_id}/items/{item_id}", response_model=InventoryItemRead)
async def update_item(
    inventory_id: int,
    item_id: int,
    body: InventoryItemUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await _get_user_inventory(inventory_id, user_id, session)
    result = await session.execute(
        select(InventoryItem).where(
            InventoryItem.id == item_id,
            InventoryItem.inventory_id == inventory_id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    await session.commit()
    await session.refresh(item)
    return item


@router.delete("/{inventory_id}/items/{item_id}", status_code=204)
async def remove_item(
    inventory_id: int,
    item_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await _get_user_inventory(inventory_id, user_id, session)
    result = await session.execute(
        select(InventoryItem).where(
            InventoryItem.id == item_id,
            InventoryItem.inventory_id == inventory_id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(item)
    await session.commit()
