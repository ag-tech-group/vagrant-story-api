"""seed enemy bestiary data

Revision ID: j4k5l6m7n8o9
Revises: i3j4k5l6m7n8
Create Date: 2026-03-25 18:00:00.000000

"""

import json
from collections.abc import Sequence
from pathlib import Path

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "j4k5l6m7n8o9"
down_revision: str | Sequence[str] | None = "i3j4k5l6m7n8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# New areas needed for enemy encounter locations (not in the a7b8c9d0e1f2 migration)
NEW_AREAS = [
    "City Walls East",
    "City Walls North",
    "City Walls South",
    "City Walls West",
    "Game Intro",
    "Great Cathedral Dome",
    "The Keep Time Trials",
]


def upgrade() -> None:
    """Seed all enemy/bestiary data from JSON files."""
    conn = op.get_bind()

    # ── Step 1: Insert new areas ──────────────────────────────────
    for area_name in NEW_AREAS:
        conn.execute(
            sa.text(
                "INSERT INTO areas (name) SELECT :name_val "
                "WHERE NOT EXISTS (SELECT 1 FROM areas WHERE name = :name_check)"
            ),
            {"name_val": area_name, "name_check": area_name},
        )

    # ── Step 2: Insert new rooms from encounter_room_mapping ──────
    mapping_data = json.loads((DATA_DIR / "encounter_room_mapping.json").read_text())
    # Collect unique new rooms (created match_type)
    new_rooms: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for entry in mapping_data.values():
        if entry["match_type"] == "created":
            pair = (entry["api_area"], entry["api_room"])
            if pair not in seen:
                seen.add(pair)
                new_rooms.append(pair)
    new_rooms.sort()

    for area_name, room_name in new_rooms:
        conn.execute(
            sa.text(
                "INSERT INTO rooms (area_id, name) "
                "SELECT a.id, :room_val FROM areas a WHERE a.name = :area_name "
                "AND NOT EXISTS ("
                "  SELECT 1 FROM rooms r "
                "  JOIN areas a2 ON r.area_id = a2.id "
                "  WHERE a2.name = :area_check AND r.name = :room_check"
                ")"
            ),
            {
                "area_name": area_name,
                "room_val": room_name,
                "area_check": area_name,
                "room_check": room_name,
            },
        )

    # ── Step 3: Insert enemies ────────────────────────────────────
    enemies_data = json.loads((DATA_DIR / "enemies.json").read_text())

    for enemy in enemies_data:
        conn.execute(
            sa.text(
                'INSERT INTO enemies (name, enemy_class, hp, mp, "str", "int", "agi", '
                "encyclopaedia_number, description, movement, is_boss) "
                "VALUES (:name, :enemy_class, :hp, :mp, :str, :int, :agi, "
                ":encyclopaedia_number, :description, :movement, :is_boss)"
            ),
            {
                "name": enemy["name"],
                "enemy_class": enemy["enemy_class"],
                "hp": enemy["hp"],
                "mp": enemy["mp"],
                "str": enemy["str"],
                "int": enemy["int"],
                "agi": enemy["agi"],
                "encyclopaedia_number": enemy.get("encyclopaedia_number"),
                "description": enemy.get("description", ""),
                "movement": enemy.get("movement", 0),
                "is_boss": enemy.get("is_boss", False),
            },
        )

    # ── Step 4: Insert enemy body parts ───────────────────────────
    # Build enemy name -> id lookup
    enemy_rows = conn.execute(sa.text("SELECT id, name FROM enemies")).fetchall()
    enemy_name_to_id: dict[str, int] = {row[1]: row[0] for row in enemy_rows}

    for enemy in enemies_data:
        enemy_id = enemy_name_to_id.get(enemy["name"])
        if not enemy_id:
            continue
        for bp in enemy.get("body_parts", []):
            conn.execute(
                sa.text(
                    "INSERT INTO enemy_body_parts "
                    "(enemy_id, name, physical, air, fire, earth, water, light, dark, "
                    "blunt, edged, piercing, evade, chain_evade) "
                    "VALUES (:enemy_id, :name, :physical, :air, :fire, :earth, :water, "
                    ":light, :dark, :blunt, :edged, :piercing, :evade, :chain_evade)"
                ),
                {
                    "enemy_id": enemy_id,
                    "name": bp["name"],
                    "physical": bp["physical"],
                    "air": bp["air"],
                    "fire": bp["fire"],
                    "earth": bp["earth"],
                    "water": bp["water"],
                    "light": bp["light"],
                    "dark": bp["dark"],
                    "blunt": bp["blunt"],
                    "edged": bp["edged"],
                    "piercing": bp["piercing"],
                    "evade": bp.get("evade", 0),
                    "chain_evade": bp.get("chain_evade", 0),
                },
            )

    # ── Step 5: Insert enemy drops ────────────────────────────────
    drops_data = json.loads((DATA_DIR / "enemy_drops.json").read_text())

    for entry in drops_data:
        enemy_id = enemy_name_to_id.get(entry["enemy_name"])
        if not enemy_id:
            continue
        for drop in entry["drops"]:
            conn.execute(
                sa.text(
                    "INSERT INTO enemy_drops "
                    "(enemy_id, body_part, item, material, drop_chance, drop_value, "
                    "grip, quantity) "
                    "VALUES (:enemy_id, :body_part, :item, :material, :drop_chance, "
                    ":drop_value, :grip, :quantity)"
                ),
                {
                    "enemy_id": enemy_id,
                    "body_part": drop["body_part"],
                    "item": drop["item"],
                    "material": drop.get("material", ""),
                    "drop_chance": drop["drop_chance"],
                    "drop_value": drop.get("drop_value", 0),
                    "grip": drop.get("grip", ""),
                    "quantity": drop.get("quantity", 1),
                },
            )

    # ── Step 6: Insert enemy encounters ───────────────────────────
    encounters_data = json.loads((DATA_DIR / "enemy_encounters.json").read_text())

    # Build room lookup from DB: (area_name, room_name) -> room_id
    room_rows = conn.execute(
        sa.text(
            "SELECT r.id, a.name AS area_name, r.name AS room_name "
            "FROM rooms r JOIN areas a ON r.area_id = a.id"
        )
    ).fetchall()
    db_room_lookup: dict[tuple[str, str], int] = {(row[1], row[2]): row[0] for row in room_rows}

    # Build FAQ key -> room_id using the mapping's api_area/api_room to find DB room
    faq_to_room_id: dict[str, int] = {}
    for key, entry in mapping_data.items():
        api_area = entry.get("api_area")
        api_room = entry.get("api_room")
        if api_area and api_room:
            room_id = db_room_lookup.get((api_area, api_room))
            if room_id:
                faq_to_room_id[key] = room_id

    for enc in encounters_data:
        enemy_id = enemy_name_to_id.get(enc["enemy_name"])
        if not enemy_id:
            continue

        faq_key = f"{enc['area']} :: {enc['room']}"
        room_id = faq_to_room_id.get(faq_key)
        if not room_id:
            continue

        attacks = ", ".join(enc.get("attacks", []))
        condition = enc.get("condition", "")

        result = conn.execute(
            sa.text(
                "INSERT INTO enemy_encounters (enemy_id, room_id, condition, attacks) "
                "VALUES (:enemy_id, :room_id, :condition, :attacks) RETURNING id"
            ),
            {
                "enemy_id": enemy_id,
                "room_id": room_id,
                "condition": condition,
                "attacks": attacks,
            },
        )
        encounter_id = result.scalar_one()

        # ── Step 7: Insert encounter drops ────────────────────────
        for drop_data in enc.get("drops", []):
            drop_item = drop_data.get("item", "")
            drop_chance = drop_data.get("drop_chance", "")
            if not drop_item or drop_chance == "never":
                continue
            conn.execute(
                sa.text(
                    "INSERT INTO encounter_drops "
                    "(encounter_id, body_part, item, material, drop_chance, drop_value, "
                    "grip, quantity) "
                    "VALUES (:encounter_id, :body_part, :item, :material, :drop_chance, "
                    ":drop_value, :grip, :quantity)"
                ),
                {
                    "encounter_id": encounter_id,
                    "body_part": drop_data.get("body_part", ""),
                    "item": drop_item,
                    "material": drop_data.get("material", "") or "",
                    "drop_chance": drop_chance,
                    "drop_value": drop_data.get("drop_value") or 0,
                    "grip": drop_data.get("grip", "") or "",
                    "quantity": drop_data.get("quantity", 1) or 1,
                },
            )


def downgrade() -> None:
    """Remove all seeded enemy/bestiary data."""
    conn = op.get_bind()

    # Delete in reverse FK order
    conn.execute(sa.text("DELETE FROM encounter_drops"))
    conn.execute(sa.text("DELETE FROM enemy_encounters"))
    conn.execute(sa.text("DELETE FROM enemy_drops"))
    conn.execute(sa.text("DELETE FROM enemy_body_parts"))
    conn.execute(sa.text("DELETE FROM enemies"))

    # Remove the new rooms (those in new areas + created rooms in existing areas)
    new_area_names = [
        "City Walls East",
        "City Walls North",
        "City Walls South",
        "City Walls West",
        "Game Intro",
        "Great Cathedral Dome",
        "The Keep Time Trials",
    ]

    # Delete rooms in new areas
    conn.execute(
        sa.text(
            "DELETE FROM rooms WHERE area_id IN (SELECT id FROM areas WHERE name = ANY(:names))"
        ),
        {"names": new_area_names},
    )

    # Delete rooms that were created for existing areas (from encounter_room_mapping)
    mapping_data = json.loads((DATA_DIR / "encounter_room_mapping.json").read_text())
    for entry in mapping_data.values():
        if entry["match_type"] == "created" and entry["api_area"] not in new_area_names:
            conn.execute(
                sa.text(
                    "DELETE FROM rooms WHERE name = :room_name "
                    "AND area_id = (SELECT id FROM areas WHERE name = :area_name)"
                ),
                {"room_name": entry["api_room"], "area_name": entry["api_area"]},
            )

    # Delete the new areas
    conn.execute(
        sa.text("DELETE FROM areas WHERE name = ANY(:names)"),
        {"names": new_area_names},
    )
