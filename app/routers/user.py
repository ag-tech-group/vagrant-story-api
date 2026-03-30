from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_async_session
from app.models.armor import Armor
from app.models.blade import Blade
from app.models.consumable import Consumable
from app.models.gem import Gem
from app.models.grip import Grip
from app.models.inventory import Inventory, InventoryItem
from app.schemas.game_data import (
    GameSaveImportRequest,
    GameSaveImportResponse,
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


VALID_ITEM_TYPES = {"blade", "grip", "armor", "gem", "consumable"}


@router.post("/import-save", response_model=GameSaveImportResponse, status_code=201)
async def import_save(
    body: GameSaveImportRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create an inventory from a parsed game save file.

    Items are identified by field_name (a stable game data identifier)
    rather than database IDs. The server resolves field_names to database
    records, making this endpoint safe to call from any client without
    knowledge of the database schema.
    """
    warnings: list[str] = []

    # Build field_name → DB record lookup maps
    blades_by_fn = {b.field_name: b for b in (await session.execute(select(Blade))).scalars().all()}
    grips_by_fn = {g.field_name: g for g in (await session.execute(select(Grip))).scalars().all()}
    armor_by_fn = {a.field_name: a for a in (await session.execute(select(Armor))).scalars().all()}
    gems_by_fn = {g.field_name: g for g in (await session.execute(select(Gem))).scalars().all()}
    consumables_by_fn = {
        c.field_name: c for c in (await session.execute(select(Consumable))).scalars().all()
    }

    type_to_map: dict[str, dict] = {
        "blade": blades_by_fn,
        "grip": grips_by_fn,
        "armor": armor_by_fn,
        "gem": gems_by_fn,
        "consumable": consumables_by_fn,
    }

    # Create inventory (flush to get ID without committing)
    inventory = Inventory(
        user_id=user_id,
        name=body.name,
        base_hp=body.base_hp,
        base_mp=body.base_mp,
        base_str=body.base_str,
        base_int=body.base_int,
        base_agi=body.base_agi,
    )
    session.add(inventory)
    await session.flush()

    # Resolve items by field_name and create InventoryItems
    seen_slots: set[str] = set()
    new_items: list[InventoryItem] = []

    for idx, item_data in enumerate(body.items):
        if item_data.item_type not in VALID_ITEM_TYPES:
            warnings.append(f"Item {idx}: unknown item_type '{item_data.item_type}', skipped")
            continue

        if item_data.storage not in VALID_STORAGE:
            warnings.append(
                f"Item {idx} ({item_data.field_name}): invalid storage '{item_data.storage}', skipped"
            )
            continue

        # Resolve main item
        lookup_map = type_to_map[item_data.item_type]
        record = lookup_map.get(item_data.field_name)
        if not record:
            warnings.append(
                f"Item {idx}: {item_data.item_type} '{item_data.field_name}' not found, skipped"
            )
            continue

        # Resolve grip (for assembled weapons)
        grip_id: int | None = None
        if item_data.grip_field_name:
            grip_record = grips_by_fn.get(item_data.grip_field_name)
            if grip_record:
                grip_id = grip_record.id
            else:
                warnings.append(
                    f"Item {idx} ({item_data.field_name}): grip '{item_data.grip_field_name}' not found"
                )

        # Resolve gems (up to 3)
        gem_ids: list[int | None] = [None, None, None]
        for gi, gem_fn in enumerate(item_data.gem_field_names[:3]):
            if gem_fn:
                gem_record = gems_by_fn.get(gem_fn)
                if gem_record:
                    gem_ids[gi] = gem_record.id
                else:
                    warnings.append(
                        f"Item {idx} ({item_data.field_name}): gem '{gem_fn}' not found"
                    )

        # Validate equip_slot
        equip_slot = item_data.equip_slot
        if equip_slot is not None:
            if item_data.storage != "bag":
                equip_slot = None
            elif equip_slot not in VALID_EQUIP_SLOTS:
                warnings.append(
                    f"Item {idx} ({item_data.field_name}): invalid equip_slot '{equip_slot}', clearing"
                )
                equip_slot = None
            elif equip_slot in seen_slots:
                warnings.append(
                    f"Item {idx} ({item_data.field_name}): duplicate equip_slot '{equip_slot}', clearing"
                )
                equip_slot = None

        if equip_slot:
            seen_slots.add(equip_slot)

        # Accessories don't have meaningful materials
        material = item_data.material
        if item_data.item_type == "armor" and getattr(record, "armor_type", None) == "Accessory":
            material = None

        new_items.append(
            InventoryItem(
                inventory_id=inventory.id,
                item_type=item_data.item_type,
                item_id=record.id,
                material=material,
                grip_id=grip_id,
                gem_1_id=gem_ids[0],
                gem_2_id=gem_ids[1],
                gem_3_id=gem_ids[2],
                equip_slot=equip_slot,
                storage=item_data.storage,
                quantity=item_data.quantity,
            )
        )

    session.add_all(new_items)
    await session.commit()
    await session.refresh(inventory)

    return GameSaveImportResponse(inventory=inventory, warnings=warnings)


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
