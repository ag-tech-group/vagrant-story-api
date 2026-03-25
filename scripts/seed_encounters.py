"""Seed missing rooms/areas and enemy encounters from encounter data.

Usage:
    PYTHONPATH=. uv run python scripts/seed_encounters.py
"""

import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.area import Area
from app.models.enemy import Enemy
from app.models.enemy_encounter import EnemyEncounter
from app.models.room import Room

DATA_DIR = Path(__file__).parent.parent / "data"

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed_missing_rooms_and_areas(session: AsyncSession) -> dict[str, int]:
    """Create missing areas and rooms from the encounter room mapping.

    Returns updated mapping of 'Area :: Room' -> room_id.
    """
    mapping_path = DATA_DIR / "encounter_room_mapping.json"
    mapping = json.loads(mapping_path.read_text())

    # Build existing area name -> id map
    result = await session.execute(select(Area))
    area_map: dict[str, int] = {a.name: a.id for a in result.scalars().all()}

    # Build existing room (area_id, room_name) -> room_id map
    result = await session.execute(select(Room))
    room_map: dict[tuple[int, str], int] = {
        (r.area_id, r.name): r.id for r in result.scalars().all()
    }

    # Collect new areas and rooms needed
    new_areas: set[str] = set()
    new_rooms: set[tuple[str, str]] = set()  # (area_name, room_name)

    for key, entry in mapping.items():
        if entry["room_id"] is not None:
            continue  # already matched
        area_name, room_name = key.split(" :: ", 1)
        if area_name not in area_map:
            new_areas.add(area_name)
        new_rooms.add((area_name, room_name))

    # Create new areas
    areas_created = 0
    for area_name in sorted(new_areas):
        area = Area(name=area_name)
        session.add(area)
        await session.flush()
        area_map[area_name] = area.id
        areas_created += 1

    if areas_created:
        print(f"  Created {areas_created} new areas")

    # Create new rooms
    rooms_created = 0
    for area_name, room_name in sorted(new_rooms):
        area_id = area_map.get(area_name)
        if not area_id:
            print(f"  WARNING: Area '{area_name}' not found, skipping room '{room_name}'")
            continue
        if (area_id, room_name) in room_map:
            continue  # room already exists
        room = Room(area_id=area_id, name=room_name)
        session.add(room)
        await session.flush()
        room_map[(area_id, room_name)] = room.id
        rooms_created += 1

    if rooms_created:
        print(f"  Created {rooms_created} new rooms")

    await session.commit()

    # Build the final key -> room_id mapping and update the JSON file
    updated = False
    for key, entry in mapping.items():
        if entry["room_id"] is not None:
            continue
        area_name, room_name = key.split(" :: ", 1)
        area_id = area_map.get(area_name)
        if area_id:
            room_id = room_map.get((area_id, room_name))
            if room_id:
                entry["room_id"] = room_id
                entry["api_area"] = area_name
                entry["api_room"] = room_name
                if entry["match_type"] == "no_match":
                    entry["match_type"] = "created"
                elif entry["match_type"] == "area_only":
                    entry["match_type"] = "created"
                entry.pop("note", None)
                updated = True

    if updated:
        mapping_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")
        print("  Updated encounter_room_mapping.json with new room IDs")

    # Return key -> room_id for encounter seeding
    return {key: entry["room_id"] for key, entry in mapping.items() if entry["room_id"] is not None}


async def seed_encounters(session: AsyncSession, room_lookup: dict[str, int]):
    """Seed enemy encounters from enemy_encounters.json."""
    result = await session.execute(select(EnemyEncounter).limit(1))
    if result.scalar_one_or_none():
        print("  enemy_encounters: already seeded, skipping")
        return

    data_path = DATA_DIR / "enemy_encounters.json"
    if not data_path.exists():
        print("  enemy_encounters: enemy_encounters.json not found, skipping")
        return

    encounters = json.loads(data_path.read_text())

    # Build enemy name -> id map
    enemies_result = await session.execute(select(Enemy))
    name_to_id: dict[str, int] = {e.name: e.id for e in enemies_result.scalars().all()}

    total = 0
    skipped_enemy = 0
    skipped_room = 0
    for enc in encounters:
        enemy_id = name_to_id.get(enc["enemy_name"])
        if not enemy_id:
            skipped_enemy += 1
            continue

        key = f"{enc['area']} :: {enc['room']}"
        room_id = room_lookup.get(key)
        if not room_id:
            skipped_room += 1
            continue

        attacks = ", ".join(enc.get("attacks", []))
        condition = enc.get("condition", "")

        session.add(
            EnemyEncounter(
                enemy_id=enemy_id,
                room_id=room_id,
                condition=condition,
                attacks=attacks,
            )
        )
        total += 1

    await session.commit()
    print(f"  enemy_encounters: {total} encounters seeded")
    if skipped_enemy:
        print(f"    (skipped {skipped_enemy} encounters: enemy name not found)")
    if skipped_room:
        print(f"    (skipped {skipped_room} encounters: room not found)")


async def main():
    print("Seeding encounter data...")

    async with async_session() as session:
        room_lookup = await seed_missing_rooms_and_areas(session)
        await seed_encounters(session, room_lookup)

    await engine.dispose()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
