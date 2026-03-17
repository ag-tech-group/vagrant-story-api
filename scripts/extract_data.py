"""Extract game data from korobetski's Vagrant Story Unity Parser C# files.

Parses hardcoded constructor calls and outputs JSON seed files to data/.
"""

import json
import re
from pathlib import Path

DB_DIR = (
    Path.home()
    / "apps"
    / "criticalbit"
    / "data-extraction"
    / "Vagrant-Story-Unity-Parser"
    / "Assets"
    / "Scripts"
    / "Vagrant Story"
    / "Database"
)
OUT_DIR = Path(__file__).parent.parent / "data"
OUT_DIR.mkdir(exist_ok=True)

BLADE_TYPES = {
    0: "None",
    1: "Dagger",
    2: "Sword",
    3: "Great Sword",
    4: "Axe",
    5: "Mace",
    6: "Great Axe",
    7: "Staff",
    8: "Heavy Mace",
    9: "Polearm",
    10: "Crossbow",
}
DAMAGE_TYPES = {0: "None", 1: "Blunt", 2: "Edged", 3: "Piercing"}
ARMOR_TYPES = {0: "None", 1: "Shield", 2: "Helm", 3: "Body", 4: "Glove", 5: "Boots", 6: "Accessory"}


def parse_constructor_args(line: str) -> list[str]:
    """Extract arguments from a C# constructor call like new Blade("x", "y", 1, 2)."""
    match = re.search(r"new \w+\((.*)\)", line)
    if not match:
        return []
    args_str = match.group(1)
    # Split carefully — strings may contain commas
    args = []
    current = ""
    in_string = False
    for char in args_str:
        if char == '"' and (not current or current[-1] != "\\"):
            in_string = not in_string
            current += char
        elif char == "," and not in_string:
            args.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        args.append(current.strip())
    return args


def clean_str(s: str) -> str:
    """Remove quotes from a string arg."""
    return s.strip('"').replace('\\"', '"')


def to_int(s: str) -> int:
    """Convert string to int, handling negative numbers."""
    return int(s.strip())


def get_field_name(line: str) -> str:
    """Extract the C# field name from 'public static Blade FieldName = ...'"""
    match = re.search(r"public static \w+ (\w+)\s*=", line)
    return match.group(1) if match else "Unknown"


def extract_blades():
    """Extract all blade (weapon) data from BladesDB.cs."""
    src = (DB_DIR / "BladesDB.cs").read_text()
    blades = []
    for line in src.splitlines():
        if "new Blade(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 12:
            continue
        field_name = get_field_name(line)
        blade = {
            "field_name": field_name,
            "name": clean_str(args[0]),
            "description_fr": clean_str(args[1]),
            "id": to_int(args[2]),
            "wep_file_id": to_int(args[3]),
            "blade_type": BLADE_TYPES.get(to_int(args[4]), "Unknown"),
            "damage_type": DAMAGE_TYPES.get(to_int(args[5]), "Unknown"),
            "risk": to_int(args[6]),
            "str": to_int(args[7]),
            "int": to_int(args[8]),
            "agi": to_int(args[9]),
            "range": to_int(args[10]),
            "damage": to_int(args[11]),
        }
        blades.append(blade)
    return blades


def extract_grips():
    """Extract grip data from GripsDB.cs."""
    src = (DB_DIR / "GripsDB.cs").read_text()
    grips = []
    for line in src.splitlines():
        if "new Grip(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 8:
            continue
        field_name = get_field_name(line)
        grip = {
            "field_name": field_name,
            "name": clean_str(args[0]),
            "description_fr": clean_str(args[1]),
            "id": to_int(args[2]),
            "wep_file_id": to_int(args[3]),
            "grip_type": to_int(args[4]),
            "str": to_int(args[5]),
            "int": to_int(args[6]),
            "agi": to_int(args[7]),
        }
        # Some grips have extra args (dp, pp)
        if len(args) >= 10:
            grip["dp"] = to_int(args[8])
            grip["pp"] = to_int(args[9])
        grips.append(grip)
    return grips


def extract_armors():
    """Extract armor and shield data from ArmorsDB.cs."""
    src = (DB_DIR / "ArmorsDB.cs").read_text()
    armors = []
    for line in src.splitlines():
        if "new Armor(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 5:
            continue
        field_name = get_field_name(line)
        armor = {
            "field_name": field_name,
            "name": clean_str(args[0]),
            "description_fr": clean_str(args[1]),
            "id": to_int(args[2]),
            "wep_file_id": to_int(args[3]),
            "armor_type": ARMOR_TYPES.get(to_int(args[4]), "Unknown"),
        }
        # Constructor with stats: (name, desc, id, wepid, type, str, int, agi, gs)
        if len(args) >= 9:
            armor["str"] = to_int(args[5])
            armor["int"] = to_int(args[6])
            armor["agi"] = to_int(args[7])
            armor["gem_slots"] = to_int(args[8])
        elif len(args) >= 6:
            # Constructor without stats: (name, desc, id, wepid, type, gs)
            armor["str"] = 0
            armor["int"] = 0
            armor["agi"] = 0
            armor["gem_slots"] = to_int(args[5])
        else:
            armor["str"] = 0
            armor["int"] = 0
            armor["agi"] = 0
            armor["gem_slots"] = 0
        armors.append(armor)
    return armors


def extract_gems():
    """Extract gem data from GemsDB.cs.
    Constructor: (name, desc, magnitude, affinity_type) or (name, magnitude, desc, affinity_type)
    """
    src = (DB_DIR / "GemsDB.cs").read_text()
    gems = []
    idx = 0
    for line in src.splitlines():
        if "new Gem(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 3:
            continue
        field_name = get_field_name(line)
        idx += 1
        # Args are all strings — (name, desc_or_magnitude, magnitude_or_desc, affinity_type)
        cleaned = [clean_str(a) for a in args]
        magnitudes = {"MINOR", "MAJOR", "EXCEP", "ATTACK", "PROTECTION"}
        # Figure out which arg is magnitude vs description
        if len(cleaned) >= 4:
            if cleaned[2] in magnitudes:
                gem = {
                    "field_name": field_name,
                    "id": idx,
                    "name": cleaned[0],
                    "description_fr": cleaned[1],
                    "magnitude": cleaned[2],
                    "affinity_type": cleaned[3],
                }
            elif cleaned[1] in magnitudes:
                gem = {
                    "field_name": field_name,
                    "id": idx,
                    "name": cleaned[0],
                    "description_fr": cleaned[2],
                    "magnitude": cleaned[1],
                    "affinity_type": cleaned[3],
                }
            else:
                gem = {
                    "field_name": field_name,
                    "id": idx,
                    "name": cleaned[0],
                    "description_fr": cleaned[1],
                    "magnitude": cleaned[2],
                    "affinity_type": cleaned[3],
                }
        else:
            gem = {
                "field_name": field_name,
                "id": idx,
                "name": cleaned[0],
                "description_fr": cleaned[1] if len(cleaned) > 1 else "",
                "magnitude": cleaned[2] if len(cleaned) > 2 else "",
            }
        gems.append(gem)
    return gems


def extract_materials():
    """Extract material data from MaterialsDB.cs."""
    src = (DB_DIR / "MaterialsDB.cs").read_text()
    materials = []
    for line in src.splitlines():
        if "new SmithMaterial(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 17:
            continue
        material = {
            "name": clean_str(args[0]),
            "tier": to_int(args[1]),
            "str_modifier": to_int(args[2]),
            "int_modifier": to_int(args[3]),
            "human": to_int(args[4]),
            "beast": to_int(args[5]),
            "undead": to_int(args[6]),
            "phantom": to_int(args[7]),
            "dragon": to_int(args[8]),
            "evil": to_int(args[9]),
            "fire": to_int(args[10]),
            "water": to_int(args[11]),
            "wind": to_int(args[12]),
            "earth": to_int(args[13]),
            "light": to_int(args[14]),
            "dark": to_int(args[15]),
            "agi_modifier": to_int(args[16]),
        }
        materials.append(material)
    return materials


def extract_misc_items():
    """Extract consumable item data from MiscItemsDB.cs.
    Constructor: new Misc("name", "desc", new List<ItemEffect>() { ... })
    Also extracts effect info from the ItemEffect constructors.
    """
    src = (DB_DIR / "MiscItemsDB.cs").read_text()
    items = []
    idx = 0
    # Join multi-line entries
    full_text = src.replace("\n", " ")
    for match in re.finditer(
        r'public static Misc (\w+)\s*=\s*new Misc\("([^"]*)",\s*"([^"]*)",\s*new List<ItemEffect>\(\)\s*\{(.*?)\}\)',
        full_text,
    ):
        idx += 1
        field_name = match.group(1)
        name = match.group(2)
        desc = match.group(3)
        effects_str = match.group(4)
        # Parse effects
        effects = []
        for eff_match in re.finditer(
            r"new ItemEffect\(ItemEffect\.Target\.(\w+),\s*ItemEffect\.Type\.(\w+),\s*ItemEffect\.Mod\.(\w+),\s*([^)]+)\)",
            effects_str,
        ):
            val = eff_match.group(4).strip()
            if "short.MaxValue" in val:
                val = 32767
            else:
                try:
                    val = int(val.replace("+", ""))
                except ValueError:
                    val = val  # Keep as string for complex expressions
            effects.append(
                {
                    "target": eff_match.group(1),
                    "type": eff_match.group(2),
                    "modifier": eff_match.group(3),
                    "value": val,
                }
            )
        items.append(
            {
                "field_name": field_name,
                "id": idx,
                "name": name,
                "description_fr": desc,
                "effects": effects,
            }
        )
    return items


def extract_spells():
    """Extract spell data from SpellsDB.cs."""
    src = (DB_DIR / "SpellsDB.cs").read_text()
    spells = []
    for line in src.splitlines():
        if "new Spell(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 2:
            continue
        field_name = get_field_name(line)
        spell = {
            "field_name": field_name,
            "name": clean_str(args[0]),
            "description_fr": clean_str(args[1]),
        }
        # Capture additional args
        for i, arg in enumerate(args[2:], start=2):
            try:
                spell[f"arg_{i}"] = to_int(arg)
            except ValueError:
                spell[f"arg_{i}"] = arg.strip().strip('"')
        spells.append(spell)
    return spells


def extract_grimoires():
    """Extract grimoire data from GrimoiresDB.cs."""
    src = (DB_DIR / "GrimoiresDB.cs").read_text()
    grimoires = []
    for line in src.splitlines():
        if "new Grimoire(" not in line or line.strip().startswith("//"):
            continue
        args = parse_constructor_args(line)
        if len(args) < 2:
            continue
        field_name = get_field_name(line)
        grimoire = {
            "field_name": field_name,
            "name": clean_str(args[0]),
            "description_fr": clean_str(args[1]),
        }
        if len(args) >= 3:
            grimoire["id"] = to_int(args[2])
        grimoires.append(grimoire)
    return grimoires


def main():
    print("Extracting Vagrant Story game data...")

    data = {
        "weapons": extract_blades(),
        "grips": extract_grips(),
        "armors": extract_armors(),
        "gems": extract_gems(),
        "materials": extract_materials(),
        "consumables": extract_misc_items(),
        "spells": extract_spells(),
        "grimoires": extract_grimoires(),
    }

    for name, items in data.items():
        out_path = OUT_DIR / f"{name}.json"
        out_path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
        print(f"  {name}: {len(items)} items → {out_path}")

    print("Done!")


if __name__ == "__main__":
    main()
