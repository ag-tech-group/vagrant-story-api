"""Extract crafting combination data from vagrant-story-combinations-data CSVs."""

import csv
import json
from pathlib import Path

CSV_DIR = (
    Path.home()
    / "apps"
    / "criticalbit"
    / "data-extraction"
    / "vagrant-story-combinations-data"
    / "csv"
)
OUT_DIR = Path(__file__).parent.parent / "data"
OUT_DIR.mkdir(exist_ok=True)

MATERIAL_ABBREVS = {
    "B": "Bronze",
    "I": "Iron",
    "H": "Hagane",
    "S": "Silver",
    "D": "Damascus",
    "L": "Leather",
    "W": "Wood",
}


def extract_blade_combinations():
    """Extract all blade (weapon) combination recipes."""
    recipes = []
    for csv_file in sorted(CSV_DIR.glob("Blade__*.csv")):
        # Parse category from filename: Blade__Dagger_Sword.csv → Dagger + Sword
        # Handle multi-word types like Great_Sword → Great Sword
        # Filename pattern: Blade__Type1_Type2.csv
        # But types can have underscores... parse from the actual enum
        category = csv_file.stem.replace("Blade__", "")

        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipes.append(
                    {
                        "category": "blade",
                        "sub_category": category,
                        "input_1": row["slot1"],
                        "input_2": row["slot2"],
                        "result": row["result"],
                        "tier_change": int(row["tier_change"]),
                        "has_swap": row["has_swap"] == "True",
                    }
                )
    return recipes


def extract_armor_combinations():
    """Extract all armor combination recipes."""
    recipes = []
    for csv_file in sorted(CSV_DIR.glob("Armor__*.csv")):
        category = csv_file.stem.replace("Armor__", "")

        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipes.append(
                    {
                        "category": "armor",
                        "sub_category": category,
                        "input_1": row["slot1"],
                        "input_2": row["slot2"],
                        "result": row["result"],
                        "tier_change": int(row["tier_change"]),
                        "has_swap": row["has_swap"] == "True",
                    }
                )
    return recipes


def extract_shield_combinations():
    """Extract shield combination recipes."""
    csv_file = CSV_DIR / "Shield__Shield_Shield.csv"
    if not csv_file.exists():
        return []
    recipes = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipes.append(
                {
                    "category": "shield",
                    "sub_category": "Shield_Shield",
                    "input_1": row["slot1"],
                    "input_2": row["slot2"],
                    "result": row["result"],
                    "tier_change": int(row["tier_change"]),
                    "has_swap": row["has_swap"] == "True",
                }
            )
    return recipes


def extract_material_combinations():
    """Extract material combination tables."""
    recipes = []
    for csv_file in sorted(CSV_DIR.glob("*_materials.csv")):
        category = csv_file.stem  # Blade_materials, Armor_materials, Shield_materials

        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipes.append(
                    {
                        "category": "material",
                        "sub_category": category,
                        "input_1": row["slot1"],
                        "input_2": row["slot2"],
                        "material_1": MATERIAL_ABBREVS.get(row["material1"], row["material1"]),
                        "material_2": MATERIAL_ABBREVS.get(row["material2"], row["material2"]),
                        "result_material": MATERIAL_ABBREVS.get(
                            row["result_material"], row["result_material"]
                        ),
                        "tier_change": int(row["tier_change"]),
                    }
                )
    return recipes


def main():
    print("Extracting crafting combination data...")

    blade_recipes = extract_blade_combinations()
    armor_recipes = extract_armor_combinations()
    shield_recipes = extract_shield_combinations()
    material_recipes = extract_material_combinations()

    all_item_recipes = blade_recipes + armor_recipes + shield_recipes
    print(
        f"  Item combinations: {len(all_item_recipes)} (blade: {len(blade_recipes)}, armor: {len(armor_recipes)}, shield: {len(shield_recipes)})"
    )
    print(f"  Material combinations: {len(material_recipes)}")

    out_path = OUT_DIR / "crafting_recipes.json"
    out_path.write_text(json.dumps(all_item_recipes, indent=2, ensure_ascii=False))
    print(f"  → {out_path}")

    mat_path = OUT_DIR / "material_recipes.json"
    mat_path.write_text(json.dumps(material_recipes, indent=2, ensure_ascii=False))
    print(f"  → {mat_path}")

    print("Done!")


if __name__ == "__main__":
    main()
