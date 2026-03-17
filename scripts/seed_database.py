"""Seed the database with extracted game data from JSON files."""

import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.armor import Armor
from app.models.consumable import Consumable
from app.models.gem import Gem
from app.models.grip import Grip
from app.models.material import Material
from app.models.weapon import Weapon

DATA_DIR = Path(__file__).parent.parent / "data"

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed_model(session: AsyncSession, model, json_file: str, field_map: dict | None = None):
    """Seed a model from a JSON file. Skip if data already exists."""
    result = await session.execute(select(model).limit(1))
    if result.scalar_one_or_none():
        print(f"  {model.__tablename__}: already seeded, skipping")
        return

    data_path = DATA_DIR / json_file
    if not data_path.exists():
        print(f"  {model.__tablename__}: {json_file} not found, skipping")
        return

    items = json.loads(data_path.read_text())

    # Build mapping: column name → ORM attribute name
    col_to_attr = {}
    for attr_name in dir(model):
        attr = getattr(model, attr_name, None)
        if hasattr(attr, "property") and hasattr(attr.property, "columns"):
            for col in attr.property.columns:
                col_to_attr[col.name] = attr_name

    for item in items:
        # Apply field renames (e.g., id -> game_id)
        if field_map:
            for json_key, model_key in field_map.items():
                if json_key in item:
                    item[model_key] = item.pop(json_key)
        # Map JSON keys (which match column names) to ORM attribute names
        mapped = {}
        for k, v in item.items():
            attr_name = col_to_attr.get(k, k)
            if attr_name in col_to_attr.values() or hasattr(model, attr_name):
                mapped[attr_name] = v
        session.add(model(**mapped))

    await session.commit()
    print(f"  {model.__tablename__}: {len(items)} items seeded")


async def main():
    print("Seeding database...")

    id_map = {"id": "game_id"}

    async with async_session() as session:
        await seed_model(session, Weapon, "weapons.json", id_map)
        await seed_model(session, Grip, "grips.json", id_map)
        await seed_model(
            session,
            Armor,
            "armor.json" if (DATA_DIR / "armor.json").exists() else "armors.json",
            id_map,
        )
        await seed_model(session, Gem, "gems.json", id_map)
        await seed_model(session, Material, "materials.json")
        await seed_model(session, Consumable, "consumables.json", id_map)

    await engine.dispose()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
