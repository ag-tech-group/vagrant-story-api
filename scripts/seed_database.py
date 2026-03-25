"""Seed the database with extracted game data from JSON files."""

import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.armor import Armor
from app.models.blade import Blade
from app.models.consumable import Consumable
from app.models.crafting_recipe import CraftingRecipe, MaterialRecipe
from app.models.enemy import Enemy, EnemyBodyPart, EnemyDrop
from app.models.gem import Gem
from app.models.grip import Grip
from app.models.material import Material

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


async def seed_enemies(session: AsyncSession):
    """Seed enemies and their body parts from JSON."""
    result = await session.execute(select(Enemy).limit(1))
    if result.scalar_one_or_none():
        print("  enemies: already seeded, skipping")
        return

    data_path = DATA_DIR / "enemies.json"
    if not data_path.exists():
        print("  enemies: enemies.json not found, skipping")
        return

    items = json.loads(data_path.read_text())

    for item in items:
        body_parts_data = item.pop("body_parts", [])
        item.pop("immunities", None)
        enemy = Enemy(
            name=item["name"],
            enemy_class=item["enemy_class"],
            hp=item["hp"],
            mp=item["mp"],
            str_stat=item["str"],
            int_stat=item["int"],
            agi_stat=item["agi"],
            encyclopaedia_number=item.get("encyclopaedia_number"),
            description=item.get("description", ""),
            movement=item.get("movement", 0),
            is_boss=item.get("is_boss", False),
        )
        session.add(enemy)
        await session.flush()

        for bp in body_parts_data:
            session.add(
                EnemyBodyPart(
                    enemy_id=enemy.id,
                    name=bp["name"],
                    physical=bp["physical"],
                    air=bp["air"],
                    fire=bp["fire"],
                    earth=bp["earth"],
                    water=bp["water"],
                    light=bp["light"],
                    dark=bp["dark"],
                    blunt=bp["blunt"],
                    edged=bp["edged"],
                    piercing=bp["piercing"],
                    evade=bp.get("evade", 0),
                    chain_evade=bp.get("chain_evade", 0),
                )
            )

    await session.commit()
    print(f"  enemies: {len(items)} enemies seeded")


async def seed_enemy_drops(session: AsyncSession):
    """Seed enemy drops from JSON, matching by enemy name."""
    result = await session.execute(select(EnemyDrop).limit(1))
    if result.scalar_one_or_none():
        print("  enemy_drops: already seeded, skipping")
        return

    data_path = DATA_DIR / "enemy_drops.json"
    if not data_path.exists():
        print("  enemy_drops: enemy_drops.json not found, skipping")
        return

    # Build name -> id map
    enemies_result = await session.execute(select(Enemy))
    name_to_id = {e.name: e.id for e in enemies_result.scalars().all()}

    items = json.loads(data_path.read_text())
    total = 0
    for entry in items:
        enemy_id = name_to_id.get(entry["enemy_name"])
        if not enemy_id:
            continue
        for drop in entry["drops"]:
            session.add(
                EnemyDrop(
                    enemy_id=enemy_id,
                    body_part=drop["body_part"],
                    item=drop["item"],
                    material=drop.get("material", ""),
                    drop_chance=drop["drop_chance"],
                    drop_value=drop.get("drop_value", 0),
                    grip=drop.get("grip", ""),
                    quantity=drop.get("quantity", 1),
                )
            )
            total += 1

    await session.commit()
    print(f"  enemy_drops: {total} drops seeded")


async def main():
    print("Seeding database...")

    id_map = {"id": "game_id"}

    async with async_session() as session:
        await seed_model(session, Blade, "weapons.json", id_map)
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
        await seed_model(session, CraftingRecipe, "crafting_recipes.json")
        await seed_model(session, MaterialRecipe, "material_recipes.json")
        await seed_enemies(session)
        await seed_enemy_drops(session)

    await engine.dispose()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
