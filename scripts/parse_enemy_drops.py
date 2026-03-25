#!/usr/bin/env python3
"""Parse enemy drop/equipment data from JTilton FAQ raw text.

Reads scraped-data-bestiary-raw.txt and produces:
  - data/enemy_drops.json  (consolidated per-enemy-type drops)
  - docs/scraped-data-enemy-drops.md  (summary report)
"""

import json
import re
from collections import defaultdict
from pathlib import Path

INPUT_FILE = (
    Path(__file__).resolve().parent.parent.parent / "docs" / "scraped-data-bestiary-raw.txt"
)
OUTPUT_JSON = Path(__file__).resolve().parent.parent / "data" / "enemy_drops.json"
OUTPUT_REPORT = (
    Path(__file__).resolve().parent.parent.parent / "docs" / "scraped-data-enemy-drops.md"
)

MATERIAL_MAP = {
    "W": "Wood",
    "L": "Leather",
    "B": "Bronze",
    "I": "Iron",
    "H": "Hagane",
    "S": "Silver",
    "D": "Damascus",
}

# Drop chance descriptors and their ranking (higher = better drop rate)
DROP_RANK = {
    "never": 0,
    "abysmal": 1,
    "remote": 2,
    "very poor": 3,
    "poor": 4,
    "fair": 5,
    "moderate": 6,
    "good": 7,
    "very good": 8,
    "excellent": 9,
    "always": 10,
}

# Known enemy names from section 3.2 (Menagerie) of the FAQ, plus named NPCs
# This is used to validate that we're parsing real enemy names
KNOWN_ENEMIES = {
    "Air Elemental (Strong)",
    "Air Elemental (Weak)",
    "Arch Dragon",
    "Asura",
    "Basilisk",
    "Bat",
    "Bejart",
    "Blood Lizard",
    "Crimson Blade (Type A)",
    "Crimson Blade (Type B)",
    "Crimson Blade (Type C)",
    "Crimson Blade (Type D)",
    "Crimson Blade (Type E)",
    "Crimson Blade (Type F)",
    "Crimson Blade (Type G)",
    "Crimson Blade (Type H)",
    "Crimson Blade (Type I)",
    "Crimson Blade (Type J)",
    "Crimson Blade (Type K)",
    "Damascus Crab",
    "Damascus Golem",
    "Dao",
    "Dark Crusader (Strong)",
    "Dark Crusader (Weak)",
    "Dark Dragon",
    "Dark Elemental (Strong)",
    "Dark Elemental (Weak)",
    "Dark Eye",
    "Dark Skeleton",
    "Death",
    "Djinn",
    "Dragon",
    "Dragon Zombie",
    "Dullahan (Strong)",
    "Dullahan (Weak)",
    "Dummy (Affinity)",
    "Dummy (Beast)",
    "Dummy (Dragon)",
    "Dummy (Evil)",
    "Dummy (Human)",
    "Dummy (Phantom)",
    "Dummy (Undead)",
    "Earth Dragon",
    "Earth Elemental (Strong)",
    "Earth Elemental (Weak)",
    "Fire Elemental (Strong)",
    "Fire Elemental (Weak)",
    "Flame Dragon",
    "Gargoyle",
    "Ghast",
    "Ghost (Strong)",
    "Ghost (Weak)",
    "Ghoul (One Arm)",
    "Ghoul (Two Arm)",
    "Giant Crab",
    "Goblin",
    "Goblin Leader",
    "Golem",
    "Gremlin",
    "Harpy (Strong)",
    "Harpy (Weak)",
    "Hellhound",
    "Ichthious",
    "Ifrit",
    "Imp",
    "Iron Crab",
    "Iron Golem",
    "Last Crusader (Strong)",
    "Last Crusader (Weak)",
    "Lich",
    "Lich Lord",
    "Lizardman (Strong)",
    "Lizardman (Weak)",
    "Marid",
    "Mimic",
    "Minotaur",
    "Minotaur Lord",
    "Minotaur Zombie",
    "Mummy",
    "Nightmare",
    "Nightstalker (Strong)",
    "Nightstalker (Weak)",
    "Ogre (Strong)",
    "Ogre (Weak)",
    "Ogre Lord (Strong)",
    "Ogre Lord (Weak)",
    "Ogre Zombie",
    "Orc",
    "Orc Leader",
    "Poison Slime (Strong)",
    "Poison Slime (Weak)",
    "Quicksilver",
    "Ravana",
    "Shadow",
    "Shrieker",
    "Silver Wolf",
    "Skeleton (One Arm)",
    "Skeleton (Two Arm)",
    "Skeleton Knight",
    "Sky Dragon",
    "Slime (Strong)",
    "Slime (Weak)",
    "Snow Dragon",
    "Stirge",
    "Water Elemental (Strong)",
    "Water Elemental (Weak)",
    "Wraith",
    "Wyvern (Strong)",
    "Wyvern (Weak)",
    "Wyvern Knight",
    "Wyvern Queen",
    "Zombie (One Arm)",
    "Zombie (Two Arm)",
    "Zombie Fighter",
    "Zombie Knight (One Arm)",
    "Zombie Knight (Two Arm)",
    "Zombie Mage",
    # Named NPCs/bosses that are not in the menagerie but appear as enemies
    "Duane",
    "Grissom",
    "Mandel",
    "Sackheim",
    "Goodwin",
    "Sarjik",
    "Sydney",
    "Rosencrantz",
    "Neesa",
    "Tieger",
    "Kali",
    "Guildenstern (Form 1)",
    "Guildenstern (Form 2)",
    # Intro enemies
    "Mullenkamp Soldier (Type 1)",
    "Mullenkamp Soldier (Type 2)",
}


def parse_drop_chance(text: str):
    """Parse drop chance text like 'poor (16)' into (chance_str, value)."""
    text = text.strip()
    if not text:
        return None, None
    if text == "never":
        return "never", 0
    if text == "always":
        return "always", 255
    # Match patterns like "very poor (8)", "good (32)", "abysmal (1)"
    m = re.match(r"([\w\s]+?)\s*\((\d+)\)", text)
    if m:
        return m.group(1).strip(), int(m.group(2))
    # Just a word with no number
    return text.strip(), None


def parse_encounters(lines: list[str]):
    """Parse section 4.2 of the FAQ, yielding (enemy_name, equipment_lines) tuples.

    Strategy: forward-scan for enemy name lines (6-space indented, matching known
    enemy names), then find the equipment table header, then collect equipment lines.
    """
    # Find start of section 4.2
    start_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^4\.2\.\s+The List", line):
            start_idx = i
            break
    if start_idx is None:
        raise ValueError("Could not find section 4.2")

    # Find end of section 4 (start of section 5)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if re.match(r"^5\.\s+", lines[i]):
            end_idx = i
            break

    section_lines = lines[start_idx:end_idx]

    # First pass: identify all enemy name line indices
    # Enemy names are indented 6 spaces and followed (within a few lines) by the
    # equipment table header "------- -Equipment---"
    encounters = []
    i = 0
    while i < len(section_lines):
        line = section_lines[i]
        stripped = line.strip()

        # Check if this looks like an enemy name line:
        # - Indented with spaces (typically 6)
        # - Not a room feature line (those start with *)
        # - Not a separator line
        # - Followed eventually by an equipment header
        if stripped and stripped in KNOWN_ENEMIES:
            enemy_name = stripped
            # Look ahead for the equipment header
            j = i + 1
            found_header = False
            while j < len(section_lines) and j < i + 15:
                if re.search(r"-{4,}\s+-Equipment-", section_lines[j]):
                    found_header = True
                    break
                # Stop if we hit a room separator or another enemy
                jstripped = section_lines[j].strip()
                if jstripped.startswith("=") or jstripped.startswith("%"):
                    break
                j += 1

            if found_header:
                # Collect equipment lines after the header
                j += 1  # skip the header line
                equip_lines = []
                while j < len(section_lines):
                    eline = section_lines[j]
                    estripped = eline.strip()

                    if not estripped:
                        break
                    if (
                        estripped.startswith("=")
                        or estripped.startswith("%")
                        or estripped.startswith("*")
                    ):
                        break
                    # Equipment lines have | separators
                    if "|" not in eline:
                        break

                    equip_lines.append(eline)
                    j += 1

                encounters.append((enemy_name, equip_lines))
                i = j
                continue

        i += 1

    return encounters


def parse_equipment_block(equip_lines: list[str]):
    """Parse equipment lines for a single encounter into structured drop data."""
    drops = []
    current_weapon = None

    for line in equip_lines:
        # Split on | delimiters
        parts = line.split("|")
        if len(parts) < 3:
            continue

        body_part_raw = parts[0].strip()
        equipment_raw = parts[1].strip()
        drop_chance_raw = parts[2].strip()

        # Handle grip/gem lines (body_part is "grip" or "gem", or empty with + prefix)
        if body_part_raw.lower() in ("grip", "gem", ""):
            if "+" in equipment_raw:
                sub_name = equipment_raw.lstrip("+ ").strip()
                if current_weapon is not None:
                    if body_part_raw.lower() == "gem":
                        current_weapon["gem"] = sub_name
                    else:
                        current_weapon["grip"] = sub_name
            continue

        # Normalize named weapons in quotes (e.g., "Shillelagh", "Angel Wing")
        # These are weapon slots with custom names
        if body_part_raw.startswith('"') and body_part_raw.endswith('"'):
            body_part_raw = "Weapon"

        body_part = body_part_raw

        # Parse equipment: check for material code like (B) or (L)
        if not equipment_raw:
            # No equipment on this body part
            current_weapon = None
            continue

        # Check for grip/gem continuation line (starts with "+")
        if equipment_raw.startswith("+"):
            sub_name = equipment_raw[1:].strip()
            if current_weapon is not None:
                current_weapon["grip"] = sub_name
            continue

        # Parse material and item name
        material = None
        item_name = equipment_raw
        mat_match = re.match(r"\(([WLBIHSD])\)\s+(.+)", equipment_raw)
        if mat_match:
            material = MATERIAL_MAP.get(mat_match.group(1), mat_match.group(1))
            item_name = mat_match.group(2).strip()

        # Parse drop chance
        chance_str, chance_val = parse_drop_chance(drop_chance_raw)

        if chance_str == "never":
            # Still track as current_weapon if it's a weapon (for grip lines)
            if body_part in ("Weapon",):
                current_weapon = {"_skip": True}
            else:
                current_weapon = None
            continue

        # Build drop entry
        drop = {
            "body_part": body_part,
            "item": item_name,
        }
        if material:
            drop["material"] = material
        if chance_str:
            drop["drop_chance"] = chance_str
        if chance_val is not None:
            drop["drop_value"] = chance_val

        # Handle "Misc Item" entries: may have quantity like "3 x Cure Bulb"
        if body_part == "Misc Item":
            drop["body_part"] = "Misc"
            qty_match = re.match(r"(\d+)\s*x\s+(.+)", item_name)
            if qty_match:
                drop["quantity"] = int(qty_match.group(1))
                drop["item"] = qty_match.group(2).strip()

        # Track weapon/shield for grip/gem association
        if body_part in ("Weapon", "Shield"):
            current_weapon = drop
        else:
            current_weapon = None

        drops.append(drop)

    return drops


def make_drop_key(drop: dict) -> str:
    """Create a unique key for deduplication."""
    parts = [drop["body_part"], drop["item"]]
    if "material" in drop:
        parts.append(drop["material"])
    if "grip" in drop:
        parts.append(drop["grip"])
    return "|".join(parts)


def merge_drops(all_drops_for_enemy: list[list[dict]]) -> list[dict]:
    """Merge drops from multiple encounters, keeping best drop chance per item."""
    merged = {}

    for encounter_drops in all_drops_for_enemy:
        for drop in encounter_drops:
            key = make_drop_key(drop)
            if key not in merged:
                merged[key] = dict(drop)
            else:
                # Keep the best drop chance (highest value)
                existing = merged[key]
                existing_rank = DROP_RANK.get(existing.get("drop_chance", "never"), 0)
                new_rank = DROP_RANK.get(drop.get("drop_chance", "never"), 0)

                if new_rank > existing_rank:
                    merged[key]["drop_chance"] = drop["drop_chance"]
                    merged[key]["drop_value"] = drop.get("drop_value")
                elif new_rank == existing_rank:
                    # Same rank - keep highest numeric value
                    existing_val = existing.get("drop_value", 0) or 0
                    new_val = drop.get("drop_value", 0) or 0
                    if new_val > existing_val:
                        merged[key]["drop_value"] = new_val

                # Merge quantity if present (keep highest)
                if "quantity" in drop:
                    existing_qty = existing.get("quantity", 1)
                    new_qty = drop.get("quantity", 1)
                    merged[key]["quantity"] = max(existing_qty, new_qty)

                # Merge gem if present
                if "gem" in drop and "gem" not in existing:
                    merged[key]["gem"] = drop["gem"]

    return list(merged.values())


def body_part_sort_key(body_part: str) -> int:
    """Sort key for body parts in a logical order."""
    order = ["Head", "R.Arm", "L.Arm", "Body", "Legs", "Weapon", "Shield", "Accessory", "Misc"]
    try:
        return order.index(body_part)
    except ValueError:
        return 100


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    lines = text.split("\n")

    print(f"Read {len(lines)} lines from {INPUT_FILE}")

    # Parse all encounters
    encounters = parse_encounters(lines)
    print(f"Found {len(encounters)} enemy encounters")

    # Collect unique enemy names from encounters
    unique_names = {name for name, _ in encounters}
    print(f"Unique enemy names: {len(unique_names)}")
    print(f"Names: {sorted(unique_names)}")

    # Group by enemy name and collect drops
    enemy_encounters = defaultdict(list)
    encounter_count = 0

    for enemy_name, equip_lines in encounters:
        drops = parse_equipment_block(equip_lines)
        if drops:  # Only track if there are actual droppable items
            enemy_encounters[enemy_name].append(drops)
            encounter_count += 1

    print(f"\nEnemies with drops across encounters: {len(enemy_encounters)}")
    print(f"Total encounters with drops: {encounter_count}")

    # Consolidate per enemy type
    result = []
    all_items = set()
    all_equipment = set()
    all_misc = set()
    material_counts = defaultdict(int)

    for enemy_name in sorted(enemy_encounters.keys()):
        all_encounter_drops = enemy_encounters[enemy_name]
        merged = merge_drops(all_encounter_drops)

        # Sort drops by body part
        merged.sort(key=lambda d: body_part_sort_key(d["body_part"]))

        entry = {
            "enemy_name": enemy_name,
            "drops": merged,
        }
        result.append(entry)

        for drop in merged:
            all_items.add(drop["item"])
            if drop["body_part"] == "Misc":
                all_misc.add(drop["item"])
            else:
                all_equipment.add(drop["item"])
                if "material" in drop:
                    material_counts[drop["material"]] += 1

    # Write JSON output
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(result)} enemy entries to {OUTPUT_JSON}")

    # Generate summary report
    report_lines = [
        "# Enemy Drop Data - Parsing Summary",
        "",
        "Source: `scraped-data-bestiary-raw.txt` (JTilton Vagrant Story Enemy Guide)",
        "",
        "## Stats",
        "",
        f"- **Total enemy encounters parsed:** {len(encounters)}",
        f"- **Encounters with droppable items:** {encounter_count}",
        f"- **Unique enemy types with drops:** {len(result)}",
        f"- **Total unique items (equipment + misc):** {len(all_items)}",
        f"- **Unique equipment pieces:** {len(all_equipment)}",
        f"- **Unique misc/consumable items:** {len(all_misc)}",
        "",
        "## Materials Breakdown",
        "",
        "| Material | Equipment Count |",
        "|----------|----------------|",
    ]
    for mat in ["Wood", "Leather", "Bronze", "Iron", "Hagane", "Silver", "Damascus"]:
        count = material_counts.get(mat, 0)
        report_lines.append(f"| {mat} | {count} |")

    report_lines.extend(
        [
            "",
            "## Drop Chance Distribution",
            "",
        ]
    )

    # Count drop chances
    chance_counts = defaultdict(int)
    for entry in result:
        for drop in entry["drops"]:
            chance_counts[drop.get("drop_chance", "unknown")] += 1

    report_lines.append("| Drop Chance | Count |")
    report_lines.append("|-------------|-------|")
    for chance in [
        "always",
        "excellent",
        "very good",
        "good",
        "fair",
        "moderate",
        "poor",
        "very poor",
        "remote",
        "abysmal",
    ]:
        if chance in chance_counts:
            report_lines.append(f"| {chance} | {chance_counts[chance]} |")

    report_lines.extend(
        [
            "",
            "## Enemies with Drops (alphabetical)",
            "",
        ]
    )
    for entry in result:
        equip_count = sum(1 for d in entry["drops"] if d["body_part"] != "Misc")
        misc_count = sum(1 for d in entry["drops"] if d["body_part"] == "Misc")
        report_lines.append(
            f"- **{entry['enemy_name']}**: {equip_count} equipment, {misc_count} misc items"
        )

    report_lines.append("")

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"Wrote summary report to {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
