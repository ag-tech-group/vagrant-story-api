from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_async_session
from app.models.inventory import Inventory, InventoryItem
from app.schemas.game_data import (
    InventoryCreate,
    InventoryImportRequest,
    InventoryItemCreate,
    InventoryItemRead,
    InventoryItemUpdate,
    InventoryListRead,
    InventoryRead,
    InventoryUpdate,
)

router = APIRouter(prefix="/user/inventories", tags=["user"])

VALID_EQUIP_SLOTS = {"right_hand", "left_hand", "head", "body", "legs", "arms", "accessory"}
VALID_STORAGE = {"bag", "container"}


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


@router.post("/{inventory_id}/import", response_model=InventoryRead)
async def import_items(
    inventory_id: int,
    body: InventoryImportRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    inventory = await _get_user_inventory(inventory_id, user_id, session)

    # Validate storage and equip_slots, check for duplicates within the import batch
    seen_slots: set[str] = set()
    for item_data in body.items:
        if item_data.storage not in VALID_STORAGE:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid storage. Must be one of: {', '.join(sorted(VALID_STORAGE))}",
            )
        if item_data.equip_slot is not None:
            if item_data.storage != "bag":
                raise HTTPException(
                    status_code=400,
                    detail="Items with equip_slot must have storage 'bag'",
                )
            if item_data.equip_slot not in VALID_EQUIP_SLOTS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid equip_slot. Must be one of: {', '.join(sorted(VALID_EQUIP_SLOTS))}",
                )
            if item_data.equip_slot in seen_slots:
                raise HTTPException(
                    status_code=400,
                    detail=f"Duplicate equip_slot '{item_data.equip_slot}' in import batch",
                )
            seen_slots.add(item_data.equip_slot)

    if body.clear_existing:
        await session.execute(
            delete(InventoryItem).where(InventoryItem.inventory_id == inventory_id)
        )
    else:
        # Check that imported equip_slots don't conflict with existing items
        for slot in seen_slots:
            existing = await session.execute(
                select(InventoryItem).where(
                    InventoryItem.inventory_id == inventory_id,
                    InventoryItem.equip_slot == slot,
                )
            )
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=400,
                    detail=f"Equip slot '{slot}' is already occupied",
                )

    # Update character stats if provided (from save file import)
    if body.base_hp is not None:
        inventory.base_hp = body.base_hp
    if body.base_mp is not None:
        inventory.base_mp = body.base_mp
    if body.base_str is not None:
        inventory.base_str = body.base_str
    if body.base_int is not None:
        inventory.base_int = body.base_int
    if body.base_agi is not None:
        inventory.base_agi = body.base_agi

    new_items = [
        InventoryItem(inventory_id=inventory_id, **item_data.model_dump())
        for item_data in body.items
    ]
    session.add_all(new_items)
    await session.commit()
    await session.refresh(inventory)
    return inventory


@router.post("/{inventory_id}/items", response_model=InventoryItemRead, status_code=201)
async def add_item(
    inventory_id: int,
    body: InventoryItemCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await _get_user_inventory(inventory_id, user_id, session)

    if body.storage not in VALID_STORAGE:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid storage. Must be one of: {', '.join(sorted(VALID_STORAGE))}",
        )

    if body.equip_slot is not None:
        if body.storage != "bag":
            raise HTTPException(
                status_code=400,
                detail="Items with equip_slot must have storage 'bag'",
            )
        if body.equip_slot not in VALID_EQUIP_SLOTS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid equip_slot. Must be one of: {', '.join(sorted(VALID_EQUIP_SLOTS))}",
            )
        # Check that the slot is not already occupied in this inventory
        existing = await session.execute(
            select(InventoryItem).where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.equip_slot == body.equip_slot,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Equip slot '{body.equip_slot}' is already occupied",
            )

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

    if "storage" in update_data and update_data["storage"] is not None:
        if update_data["storage"] not in VALID_STORAGE:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid storage. Must be one of: {', '.join(sorted(VALID_STORAGE))}",
            )

    # Determine effective storage after update
    effective_storage = update_data.get("storage", item.storage)
    effective_equip_slot = update_data.get("equip_slot", item.equip_slot)
    if effective_equip_slot is not None and effective_storage != "bag":
        raise HTTPException(
            status_code=400,
            detail="Items with equip_slot must have storage 'bag'",
        )

    if "equip_slot" in update_data and update_data["equip_slot"] is not None:
        slot = update_data["equip_slot"]
        if slot not in VALID_EQUIP_SLOTS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid equip_slot. Must be one of: {', '.join(sorted(VALID_EQUIP_SLOTS))}",
            )
        # Check that the slot is not already occupied by another item
        existing = await session.execute(
            select(InventoryItem).where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.equip_slot == slot,
                InventoryItem.id != item_id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Equip slot '{slot}' is already occupied",
            )

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
