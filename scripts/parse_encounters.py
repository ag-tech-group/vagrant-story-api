"""Parse per-room enemy encounter data from the JTilton FAQ.

Reads scraped-data-bestiary-raw.txt and produces:
  - data/enemy_encounters.json
  - docs/scraped-data-encounter-locations.md
  - data/encounter_room_mapping.json
"""

import json
import re
from pathlib import Path

FAQ_PATH = Path(__file__).parent.parent.parent / "docs" / "scraped-data-bestiary-raw.txt"
DATA_DIR = Path(__file__).parent.parent / "data"
DOCS_DIR = Path(__file__).parent.parent.parent / "docs"

# Material code mapping
MATERIAL_CODES = {
    "W": "Wood",
    "L": "Leather",
    "B": "Bronze",
    "I": "Iron",
    "H": "Hagane",
    "S": "Silver",
    "D": "Damascus",
}

# Known areas/rooms from the migration
API_AREAS = [
    "Abandoned Mines B1",
    "Abandoned Mines B2",
    "Catacombs",
    "Escapeway",
    "Forgotten Pathway",
    "Great Cathedral B1",
    "Great Cathedral L1",
    "Great Cathedral L2",
    "Great Cathedral L3",
    "Iron Maiden B1",
    "Iron Maiden B2",
    "Iron Maiden B3",
    "Limestone Quarry",
    "Sanctum",
    "Snowfly Forest",
    "Snowfly Forest East",
    "Temple of Kiltia",
    "The Keep",
    "Town Center East",
    "Town Center South",
    "Town Center West",
    "Undercity East",
    "Undercity West",
    "Wine Cellar",
]

API_ROOMS = [
    ("Abandoned Mines B1", "Battle's Beginning"),
    ("Abandoned Mines B1", "Coal Mine Storage"),
    ("Abandoned Mines B1", "Miners' Resting Hall"),
    ("Abandoned Mines B1", "Mining Regrets"),
    ("Abandoned Mines B1", "Rust in Peace"),
    ("Abandoned Mines B1", "The Battle's Beginning"),
    ("Abandoned Mines B1", "The Smeltry"),
    ("Abandoned Mines B1", "Traitor's Parting"),
    ("Abandoned Mines B2", "Acolyte's Burial Vault"),
    ("Abandoned Mines B2", "Delusions of Happiness"),
    ("Abandoned Mines B2", "Dining in Darkness"),
    ("Abandoned Mines B2", "Hidden Resources"),
    ("Abandoned Mines B2", "Suicidal Desires"),
    ("Abandoned Mines B2", "The Miner's End"),
    ("Abandoned Mines B2", "Tomb of the Reborn"),
    ("Catacombs", "Bandits' Hideout"),
    ("Catacombs", "Beast's Domain"),
    ("Catacombs", "Rodent-Ridden Chamber"),
    ("Catacombs", "The Beast's Domain"),
    ("Catacombs", "The Lamenting Mother"),
    ("Catacombs", "The Withered Spring"),
    ("Catacombs", "Withered Spring"),
    ("Escapeway", "Buried Alive"),
    ("Escapeway", "Fear and Loathing"),
    ("Escapeway", "Where Body and Soul Part"),
    ("Forgotten Pathway", "Awaiting Retribution"),
    ("Forgotten Pathway", "The Fallen Knight"),
    ("Great Cathedral B1", "Order and Chaos"),
    ("Great Cathedral B1", "Truth and Lies"),
    ("Great Cathedral L1", "A Light in the Dark"),
    ("Great Cathedral L1", "Monk's Leap"),
    ("Great Cathedral L1", "The Flayed Confessional"),
    ("Great Cathedral L1", "Where Darkness Spreads"),
    ("Great Cathedral L2", "An Arrow into Darkness"),
    ("Great Cathedral L2", "Hall of Broken Vows"),
    ("Great Cathedral L2", "Maelstrom of Malice"),
    ("Great Cathedral L2", "What Ails You, Kills You"),
    ("Great Cathedral L3", "Hopes of the Idealist"),
    ("Iron Maiden B1", "Burial"),
    ("Iron Maiden B1", "Knotting"),
    ("Iron Maiden B1", "Spanish Tickler"),
    ("Iron Maiden B1", "Starvation"),
    ("Iron Maiden B1", "The Branks"),
    ("Iron Maiden B1", "The Cauldron"),
    ("Iron Maiden B1", "The Ducking Stool"),
    ("Iron Maiden B1", "The Judas Cradle"),
    ("Iron Maiden B1", "The Wheel"),
    ("Iron Maiden B2", "Lead Sprinkler"),
    ("Iron Maiden B2", "Ordeal by Fire"),
    ("Iron Maiden B2", "Pressing"),
    ("Iron Maiden B2", "Squassation"),
    ("Iron Maiden B2", "The Saw"),
    ("Iron Maiden B2", "The Shin-Vice"),
    ("Iron Maiden B3", "Dunking the Witch"),
    ("Iron Maiden B3", "Saint Elmo's Belt"),
    ("Iron Maiden B3", "The Iron Maiden"),
    ("Limestone Quarry", "Bonds of Friendship"),
    ("Limestone Quarry", "Companions in Arms"),
    ("Limestone Quarry", "Dream of the Holy Land"),
    ("Limestone Quarry", "Drowned in Fleeting Joy"),
    ("Limestone Quarry", "Excavated Hollow"),
    ("Limestone Quarry", "Hall of the Wage-Paying"),
    ("Limestone Quarry", "Stone and Sulfurous Fire"),
    ("Sanctum", "Alchemists' Laboratory"),
    ("Sanctum", "Hall of Sacrilege"),
    ("Sanctum", "The Cleansing Chantry"),
    ("Sanctum", "Theology Classroom"),
    ("Snowfly Forest", "Forest River"),
    ("Snowfly Forest", "Hewn from Nature"),
    ("Snowfly Forest", "Nature's Womb"),
    ("Snowfly Forest", "Return to the Land"),
    ("Snowfly Forest East", "Nature's Womb"),
    ("Temple of Kiltia", "Chapel of Meschaunce"),
    ("Temple of Kiltia", "Hall of Prayer"),
    ("Temple of Kiltia", "The Chapel of Meschaunce"),
    ("Temple of Kiltia", "Those who Fear the Light"),
    ("The Keep", "The Warrior's Rest"),
    ("Town Center East", "Gharmes Walk"),
    ("Town Center East", "Rue Crimnade"),
    ("Town Center East", "Rue Fisserano"),
    ("Town Center East", "The House Gilgitte"),
    ("Town Center South", "The House Khazabas"),
    ("Town Center West", "Rene Coast Road"),
    ("Town Center West", "Tircolas Flow"),
    ("Undercity East", "Arms Against Invaders"),
    ("Undercity East", "Bazaar of the Bizarre"),
    ("Undercity East", "Catspaw Blackmarket"),
    ("Undercity East", "Gemsword Blackmarket"),
    ("Undercity East", "Place of Free Words"),
    ("Undercity East", "Sale of the Sword"),
    ("Undercity East", "Weapons Not Allowed"),
    ("Undercity East", "Where Black Waters Ran"),
    ("Undercity West", "Bite The Master's Wounds"),
    ("Undercity West", "Corner of Prayers"),
    ("Undercity West", "Crumbling Market"),
    ("Undercity West", "Fear of the Fall"),
    ("Undercity West", "Larder for a Lean Winter"),
    ("Undercity West", "Nameless Dark Oblivion"),
    ("Undercity West", "Remembering Days of Yore"),
    ("Undercity West", "Sewer of Ravenous Rats"),
    ("Undercity West", "Sinner's Corner"),
    ("Undercity West", "The Children's Hideout"),
    ("Undercity West", "The Crumbling Market"),
    ("Undercity West", "The Washing-Woman's Way"),
    ("Undercity West", "Underdark Fishmarket"),
    ("Wine Cellar", "Blackmarket of Wines"),
    ("Wine Cellar", "Gallows"),
    ("Wine Cellar", "The Gallows"),
    ("Wine Cellar", "The Hero's Winehall"),
    ("Wine Cellar", "The Reckoning Room"),
    ("Wine Cellar", "Worker's Breakroom"),
]


def parse_drop_chance(text):
    """Parse drop chance string like 'poor (16)' into (chance_name, value)."""
    text = text.strip()
    if not text:
        return None, None
    m = re.match(r"([\w\s]+?)(?:\s*\((\d+)\))?$", text)
    if m:
        name = m.group(1).strip()
        val = int(m.group(2)) if m.group(2) else None
        return name, val
    return text, None


def parse_equipment_line(line):
    """Parse an equipment table line.

    Example: 'R.Arm           | (B) Chain Coif          | poor (16)      | Normal'
    Returns dict with body_part, item, material, drop_chance, drop_value, attacks.
    """
    parts = line.split("|")
    if len(parts) < 3:
        return None

    body_part = parts[0].strip()
    equipment_str = parts[1].strip()
    chance_str = parts[2].strip()
    attacks_str = parts[3].strip() if len(parts) > 3 else ""

    # Parse material and item from equipment string
    material = ""
    item = ""
    if equipment_str:
        m = re.match(r"\(([WLBIHSD])\)\s+(.+)", equipment_str)
        if m:
            material = MATERIAL_CODES.get(m.group(1), m.group(1))
            item = m.group(2).strip()
        else:
            item = equipment_str

    # Parse drop chance
    chance_name, chance_value = parse_drop_chance(chance_str)

    # Parse attacks
    attacks = []
    if attacks_str:
        attacks = [a.strip() for a in attacks_str.split(",") if a.strip()]

    return {
        "body_part": body_part,
        "item": item,
        "material": material,
        "drop_chance": chance_name,
        "drop_value": chance_value,
        "attacks": attacks,
    }


def is_area_separator(line):
    """Check if line is a %%% area separator."""
    return bool(re.match(r"^\s*%{10,}$", line.rstrip()))


def is_room_separator(line):
    """Check if line is a ====== room separator."""
    return bool(re.match(r"^\s*={10,}$", line.rstrip()))


def is_table_header(line):
    """Check if line is the '-------- -Equipment--- ...' header."""
    return "Equipment" in line and line.strip().startswith("---")


def is_equipment_data(line):
    """Check if line has | delimited equipment data."""
    return "|" in line and not line.strip().startswith("---")


def parse_faq():
    """Parse the full FAQ and extract all room-by-room encounters."""
    text = FAQ_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Find section boundaries
    # There are two occurrences of "4.2. The List" - one in the TOC and one
    # as the actual section header. We want the last one (actual section).
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "4.2. The List":
            start_idx = i  # Keep overwriting to get the last/real one
    if start_idx is not None:
        for i in range(start_idx + 1, len(lines)):
            if lines[i].strip().startswith("5. Where can I get"):
                end_idx = i
                break

    if start_idx is None or end_idx is None:
        raise ValueError("Could not find section 4.2 boundaries")

    print(f"  Section 4.2 spans lines {start_idx} to {end_idx}")
    section = lines[start_idx:end_idx]

    encounters = []
    current_area = None
    current_room = None

    i = 0
    while i < len(section):
        line = section[i]

        # ── Area header: %%% / AreaName / %%% ──
        if is_area_separator(line):
            # Expect: %%%, AreaName, %%%
            if i + 2 < len(section) and is_area_separator(section[i + 2]):
                current_area = section[i + 1].strip()
                current_room = None
                i += 3
                continue
            else:
                # Single %%% line? Skip.
                i += 1
                continue

        # ── Room separator: ====== ──
        if is_room_separator(line):
            i += 1
            continue

        # ── Room name detection ──
        # Room names are at 2-space indent, start with a letter, no |
        # They appear right after ====== or %%% blocks, or at the start of an area
        if (
            current_area is not None
            and re.match(r"^  [A-Za-z]", line)
            and "|" not in line
            and not line.strip().startswith("*")
            and not line.strip().startswith("---")
        ):
            # Verify it's really a room name by looking ahead for * bullets or ====
            candidate = line.strip()
            looks_like_room = False
            for k in range(i + 1, min(i + 15, len(section))):
                peek = section[k].strip()
                if peek == "":
                    continue
                if peek.startswith("*"):
                    looks_like_room = True
                    break
                if is_room_separator(section[k]) or is_area_separator(section[k]):
                    looks_like_room = True
                    break
                # For time trials: enemy names directly (6-space indent)
                if re.match(r"^      [A-Z]", section[k]) and "|" not in section[k]:
                    looks_like_room = True
                    break
                break

            if looks_like_room:
                current_room = candidate
                i += 1
                continue

        # ── "* Enemies:" header ──
        enemies_match = re.match(r"^\s+\*\s+Enemies:\s*(.*)", line)
        if enemies_match:
            rest = enemies_match.group(1).strip()
            if rest.lower() == "none":
                i += 1
                continue

            i += 1
            # Parse all enemies in this room section
            encounters.extend(_parse_enemies_block(section, i, current_area, current_room))

            # Advance i past the enemies block
            while i < len(section):
                ln = section[i]
                if is_room_separator(ln) or is_area_separator(ln):
                    break
                if (
                    re.match(r"^  [A-Za-z]", ln)
                    and "|" not in ln
                    and not ln.strip().startswith("*")
                ):
                    # Could be next room name
                    break
                i += 1
            continue

        # ── Time trials: enemies without "* Enemies:" header ──
        # In "The Keep Time Trials", enemies are listed directly under the area
        # header without a room name or "* Enemies:" line.
        if (
            current_area is not None
            and "Time Trial" in current_area
            and re.match(r"^      [A-Z]", line)
            and "|" not in line
            and not line.strip().startswith("---")
        ):
            room_for_trials = current_room if current_room else current_area
            encounters.extend(_parse_enemies_block(section, i, current_area, room_for_trials))
            while i < len(section):
                ln = section[i]
                if is_room_separator(ln) or is_area_separator(ln):
                    break
                if (
                    re.match(r"^  [A-Za-z]", ln)
                    and "|" not in ln
                    and not ln.strip().startswith("*")
                ):
                    break
                i += 1
            continue

        i += 1

    return encounters


def _parse_enemies_block(section, start_i, area, room):
    """Parse a block of enemy entries starting at start_i.

    Returns list of encounter dicts.
    Updates the position index externally (caller must advance).
    """
    encounters = []
    i = start_i

    while i < len(section):
        line = section[i]

        # Stop at room/area boundaries
        if is_room_separator(line) or is_area_separator(line):
            break
        # Stop at room-level bullet points for non-enemy features
        if re.match(r"^\s+\*\s+(?!Enemies)", line) and not re.match(r"^\s+\*\s+Enemies", line):
            break
        # Stop at potential room names
        if re.match(r"^  [A-Za-z]", line) and "|" not in line and not line.strip().startswith("*"):
            break

        # Enemy name: 6-space indent, starts with letter or quote
        enemy_match = re.match(r'^      ([A-Za-z"][^\n]+)', line)
        if enemy_match and "|" not in line and not line.strip().startswith("---"):
            enemy_name = enemy_match.group(1).strip()
            i += 1

            # Collect condition text (lines before the --- table header)
            condition_parts = []
            while i < len(section):
                ln = section[i]
                if is_table_header(ln):
                    break
                if is_room_separator(ln) or is_area_separator(ln):
                    break
                if (
                    re.match(r'^      [A-Za-z"]', ln)
                    and "|" not in ln
                    and not ln.strip().startswith("---")
                ):
                    # Next enemy without a table? Shouldn't happen normally.
                    break
                stripped = ln.strip()
                if stripped:
                    condition_parts.append(stripped)
                i += 1

            # Skip table header
            if i < len(section) and is_table_header(section[i]):
                i += 1

            # Parse equipment/drop lines
            drops = []
            all_attacks = []
            last_drop_added = None  # Track last added drop for grip/gem attachment
            while i < len(section):
                ln = section[i]

                # Stop conditions
                if is_room_separator(ln) or is_area_separator(ln):
                    break
                if re.match(r"^\s+\*\s+", ln) and not is_equipment_data(ln):
                    break
                # Next enemy
                if (
                    re.match(r'^      [A-Za-z"]', ln)
                    and "|" not in ln
                    and not ln.strip().startswith("---")
                ):
                    break

                # Blank line = end of this enemy's data
                if ln.strip() == "":
                    i += 1
                    break

                if is_equipment_data(ln):
                    stripped = ln.strip()

                    # Handle grip/gem sub-lines
                    if stripped.startswith("grip") or stripped.startswith("gem"):
                        parts = stripped.split("|")
                        sub_type = parts[0].strip()
                        sub_item = parts[1].strip() if len(parts) > 1 else ""
                        if sub_item.startswith("+ "):
                            sub_item = sub_item[2:].strip()
                        # Only attach to the last drop if it was actually added
                        if last_drop_added is not None:
                            if sub_type == "grip":
                                last_drop_added["grip"] = sub_item
                            elif sub_type == "gem":
                                if "gems" not in last_drop_added:
                                    last_drop_added["gems"] = []
                                last_drop_added["gems"].append(sub_item)
                        i += 1
                        continue

                    parsed = parse_equipment_line(stripped)
                    if parsed:
                        if parsed["attacks"]:
                            all_attacks.extend(parsed["attacks"])

                        body_part = parsed["body_part"]
                        item = parsed["item"]
                        material = parsed["material"]
                        chance = parsed["drop_chance"]
                        value = parsed["drop_value"]

                        # Reset last_drop_added for each new equipment line
                        last_drop_added = None

                        # Handle Misc Item with quantity
                        quantity = 1
                        if body_part == "Misc Item" and item:
                            qm = re.match(r"(\d+)\s+x\s+(.+)", item)
                            if qm:
                                quantity = int(qm.group(1))
                                item = qm.group(2).strip()

                        # Only include drops where chance is NOT "never" and item is not empty
                        if item and chance and chance != "never":
                            drop_entry = {
                                "body_part": body_part,
                                "item": item,
                                "material": material,
                                "drop_chance": chance,
                                "drop_value": value,
                            }
                            if quantity > 1:
                                drop_entry["quantity"] = quantity
                            drops.append(drop_entry)
                            last_drop_added = drop_entry

                    i += 1
                    continue

                i += 1

            # Build condition string
            condition = " ".join(condition_parts).strip()
            condition = re.sub(r"\s+", " ", condition)

            # Deduplicate attacks preserving order
            seen = set()
            unique_attacks = []
            for a in all_attacks:
                if a not in seen:
                    seen.add(a)
                    unique_attacks.append(a)

            encounter = {
                "area": area,
                "room": room,
                "enemy_name": enemy_name,
            }
            if condition:
                encounter["condition"] = condition
            encounter["drops"] = drops
            if unique_attacks:
                encounter["attacks"] = unique_attacks

            encounters.append(encounter)
            continue

        # Skip anything else
        i += 1

    return encounters


def build_room_mapping(encounters):
    """Build a mapping from FAQ (area, room) pairs to API room IDs."""
    area_id_map = {name: idx + 1 for idx, name in enumerate(API_AREAS)}
    room_id_map = {}
    for idx, (area, room) in enumerate(API_ROOMS):
        room_id_map[(area, room)] = idx + 1

    faq_rooms = set()
    for enc in encounters:
        if enc["area"] and enc["room"]:
            faq_rooms.add((enc["area"], enc["room"]))

    mapping = {}
    unmatched = []

    for faq_area, faq_room in sorted(faq_rooms):
        key = f"{faq_area} :: {faq_room}"

        # Direct match
        if (faq_area, faq_room) in room_id_map:
            mapping[key] = {
                "room_id": room_id_map[(faq_area, faq_room)],
                "api_area": faq_area,
                "api_room": faq_room,
                "match_type": "exact",
            }
            continue

        # Case-insensitive match
        found = False
        for api_area, api_room in API_ROOMS:
            if api_area.lower() == faq_area.lower() and api_room.lower() == faq_room.lower():
                mapping[key] = {
                    "room_id": room_id_map[(api_area, api_room)],
                    "api_area": api_area,
                    "api_room": api_room,
                    "match_type": "case_insensitive",
                }
                found = True
                break
        if found:
            continue

        # Try "The " prefix and suffix cleanup
        for api_area, api_room in API_ROOMS:
            if api_area != faq_area:
                continue
            clean_faq = re.sub(r"\s*\((?:early|later)\)\s*$", "", faq_room)
            candidates = [faq_room, clean_faq, f"The {faq_room}", f"The {clean_faq}"]
            # Also try removing "The " from faq_room
            if faq_room.startswith("The "):
                candidates.append(faq_room[4:])
            if clean_faq.startswith("The "):
                candidates.append(clean_faq[4:])
            for c in candidates:
                if c == api_room:
                    mapping[key] = {
                        "room_id": room_id_map[(api_area, api_room)],
                        "api_area": api_area,
                        "api_room": api_room,
                        "match_type": "fuzzy",
                    }
                    found = True
                    break
            if found:
                break
        if found:
            continue

        # Area exists but room not found
        if faq_area in area_id_map:
            mapping[key] = {
                "room_id": None,
                "api_area": faq_area,
                "api_room": None,
                "match_type": "area_only",
                "note": f"Room '{faq_room}' not found in API for area '{faq_area}'",
            }
        else:
            mapping[key] = {
                "room_id": None,
                "api_area": None,
                "api_room": None,
                "match_type": "no_match",
                "note": f"Area '{faq_area}' not found in API",
            }
        unmatched.append((faq_area, faq_room))

    return mapping, unmatched


def generate_report(encounters, mapping, unmatched):
    """Generate the summary markdown report."""
    total = len(encounters)
    areas = sorted({e["area"] for e in encounters if e["area"]})
    rooms = sorted({(e["area"], e["room"]) for e in encounters if e["area"] and e["room"]})
    unique_enemies = sorted({e["enemy_name"] for e in encounters})

    faq_areas_to_api = {}
    for area in areas:
        faq_areas_to_api[area] = area if area in API_AREAS else None

    exact = sum(1 for v in mapping.values() if v["match_type"] == "exact")
    fuzzy = sum(1 for v in mapping.values() if v["match_type"] in ("case_insensitive", "fuzzy"))
    area_only = sum(1 for v in mapping.values() if v["match_type"] == "area_only")
    no_match = sum(1 for v in mapping.values() if v["match_type"] == "no_match")

    total_drops = sum(len(e["drops"]) for e in encounters)
    encounters_with_drops = sum(1 for e in encounters if e["drops"])
    encounters_with_conditions = sum(1 for e in encounters if e.get("condition"))

    report = []
    report.append("# Enemy Encounter Locations - Parsing Report")
    report.append("")
    report.append("Parsed from the JTilton FAQ (scraped-data-bestiary-raw.txt), section 4.2.")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append(f"- **Total encounters**: {total}")
    report.append(f"- **Total unique areas**: {len(areas)}")
    report.append(f"- **Total unique rooms**: {len(rooms)}")
    report.append(f"- **Total unique enemy names**: {len(unique_enemies)}")
    report.append(f"- **Encounters with drops**: {encounters_with_drops}")
    report.append(f"- **Total droppable items**: {total_drops}")
    report.append(f"- **Encounters with conditions**: {encounters_with_conditions}")
    report.append("")
    report.append("## Area Name Mapping (FAQ to API)")
    report.append("")
    report.append("| FAQ Area | API Area | Status |")
    report.append("|----------|----------|--------|")
    for area in areas:
        api = faq_areas_to_api.get(area)
        if api:
            report.append(f"| {area} | {api} | Matched |")
        else:
            report.append(f"| {area} | - | **Not in API** |")
    report.append("")
    report.append("## Room Matching Statistics")
    report.append("")
    report.append(f"- **Exact match**: {exact}")
    report.append(f"- **Fuzzy match** (case, prefix, suffix): {fuzzy}")
    report.append(f"- **Area matched, room not found**: {area_only}")
    report.append(f"- **No match (area missing from API)**: {no_match}")
    report.append("")

    if unmatched:
        report.append("## Unmatched Rooms")
        report.append("")
        report.append("These FAQ rooms do not have a match in the existing API rooms table.")
        report.append("")
        report.append("| Area | Room |")
        report.append("|------|------|")
        for area, room in sorted(unmatched):
            report.append(f"| {area} | {room} |")
        report.append("")

    report.append("## Encounters per Area")
    report.append("")
    report.append("| Area | Encounters | Rooms |")
    report.append("|------|------------|-------|")
    for area in areas:
        area_encounters = [e for e in encounters if e["area"] == area]
        area_rooms = {e["room"] for e in area_encounters}
        report.append(f"| {area} | {len(area_encounters)} | {len(area_rooms)} |")
    report.append("")

    return "\n".join(report)


def main():
    print("Parsing FAQ encounters...")
    encounters = parse_faq()
    print(f"  Found {len(encounters)} encounters")

    areas = {e["area"] for e in encounters}
    rooms = {(e["area"], e["room"]) for e in encounters}
    print(f"  {len(areas)} unique areas, {len(rooms)} unique rooms")

    # Save encounters JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    encounters_path = DATA_DIR / "enemy_encounters.json"
    with open(encounters_path, "w") as f:
        json.dump(encounters, f, indent=2)
    print(f"  Saved {encounters_path}")

    # Build room mapping
    print("Building room mapping...")
    mapping, unmatched = build_room_mapping(encounters)
    mapping_path = DATA_DIR / "encounter_room_mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2, sort_keys=True)
    print(f"  Saved {mapping_path}")
    if unmatched:
        print(f"  {len(unmatched)} rooms could not be matched to API rooms")

    # Generate report
    print("Generating report...")
    report = generate_report(encounters, mapping, unmatched)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = DOCS_DIR / "scraped-data-encounter-locations.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Saved {report_path}")

    # Quick validation
    print("\nValidation:")
    no_area = [e for e in encounters if not e["area"]]
    no_room = [e for e in encounters if not e["room"]]
    if no_area:
        print(f"  WARNING: {len(no_area)} encounters with no area")
    if no_room:
        print(f"  WARNING: {len(no_room)} encounters with no room")
    # Print first 3 encounters as a sanity check
    print("\n  First 3 encounters:")
    for e in encounters[:3]:
        print(
            f"    {e['area']} / {e['room']} / {e['enemy_name']}: "
            f"{len(e['drops'])} drops, {len(e.get('attacks', []))} attacks"
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
