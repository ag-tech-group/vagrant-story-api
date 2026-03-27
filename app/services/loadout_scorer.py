"""Loadout optimizer scoring engine for Vagrant Story combat calculations.

Scores weapon and armor combinations against a specific enemy, considering
damage types, elemental affinities, class affinities, and body part defenses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

from app.models.armor import Armor
from app.models.blade import Blade
from app.models.enemy import Enemy, EnemyBodyPart
from app.models.grip import Grip
from app.models.inventory import InventoryItem
from app.models.material import Material

CLASS_AFFINITIES = ("human", "beast", "undead", "phantom", "dragon", "evil")
ELEMENTAL_AFFINITIES = ("fire", "water", "wind", "earth", "light", "dark")
DAMAGE_TYPES = ("blunt", "edged", "piercing")

# Armor type -> equip slot mapping (armor_type on Armor model -> conceptual slot)
ARMOR_TYPE_TO_SLOT: dict[str, str] = {
    "Helm": "helm",
    "Body": "body",
    "Leg": "legs",
    "Arm": "arms",
    "Shield": "shield",
    "Accessory": "accessory",
}


@dataclass
class OffenseScore:
    total_score: float = 0.0
    best_target: str = ""
    estimated_damage: float = 0.0
    reasoning: str = ""


@dataclass
class DefenseScore:
    total_score: float = 0.0
    estimated_reduction_pct: float = 0.0


@dataclass
class Loadout:
    rank: int = 0
    score: float = 0.0
    offense_score: float = 0.0
    defense_score: float = 0.0
    blade: Blade | None = None
    blade_material: Material | None = None
    grip: Grip | None = None
    armor_pieces: dict[str, tuple[Armor, Material]] = field(default_factory=dict)
    estimated_damage: float = 0.0
    target_body_part: str = ""
    target_reason: str = ""
    blade_inv_item_id: int | None = None
    grip_inv_item_id: int | None = None
    armor_inv_item_ids: dict[str, int] = field(default_factory=dict)


def _get_enemy_class_key(enemy_class: str) -> str | None:
    """Map enemy_class string to the affinity column name."""
    lower = enemy_class.lower()
    for key in CLASS_AFFINITIES:
        if key in lower:
            return key
    return None


def score_offense(
    blade: Blade,
    grip: Grip,
    material: Material,
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
) -> OffenseScore:
    """Score a weapon setup (blade + grip + material) against an enemy.

    For each body part, calculates effective damage considering:
    - Weapon base STR + grip STR + material blade STR modifier
    - Weapon damage stat
    - Damage type (Blunt/Edged/Piercing) vs body part damage type defense
    - Physical damage vs body part physical defense
    - Class affinity: material's class bonus matching enemy class
    - Elemental affinity: material elemental bonuses vs body part elemental defenses
    - Body part evade (lower = easier to hit = better target)
    - Chain evade (lower = better for chaining)
    """
    if not enemy_body_parts:
        return OffenseScore(reasoning="Enemy has no body parts to target")

    # Effective weapon stats
    eff_str = blade.str_stat + grip.str_stat + material.blade_str
    eff_damage = blade.damage

    # Grip bonus for the weapon's damage type
    damage_type_key = blade.damage_type.lower()
    grip_damage_bonus = getattr(grip, damage_type_key, 0) if damage_type_key in DAMAGE_TYPES else 0

    # Class affinity bonus from material
    class_key = _get_enemy_class_key(enemy.enemy_class)
    class_bonus = getattr(material, class_key, 0) if class_key else 0

    best_score = -999999.0
    best_part_name = ""
    best_damage = 0.0
    best_reason = ""

    for bp in enemy_body_parts:
        # Base physical damage: STR contributes to raw damage output
        base_damage = eff_str + eff_damage + grip_damage_bonus

        # Damage type effectiveness: negative defense on body part = weakness = bonus
        dt_defense = getattr(bp, damage_type_key, 0) if damage_type_key in DAMAGE_TYPES else 0
        # Physical defense similarly: negative = weakness
        phys_defense = bp.physical

        # dt_defense and phys_defense: positive = enemy resists, negative = enemy is weak
        # Subtracting defense means: if defense is -10 (weak), we add 10 damage
        type_factor = base_damage - dt_defense - phys_defense

        # Class affinity contribution: higher material affinity vs matching enemy class = more damage
        class_factor = class_bonus * 0.5

        # Elemental factor: sum of (material elemental - body part elemental defense)
        # If body part has negative elemental defense, that element is a weakness
        elemental_factor = 0.0
        best_element = ""
        best_element_value = 0.0
        for elem in ELEMENTAL_AFFINITIES:
            mat_elem = getattr(material, elem, 0)
            bp_elem = getattr(bp, elem, 0)
            # Material affinity bonus applied against body part defense
            # Negative bp_elem = weakness, positive mat_elem = weapon has that element
            elem_contribution = mat_elem - bp_elem
            elemental_factor += elem_contribution * 0.3
            if elem_contribution > best_element_value:
                best_element_value = elem_contribution
                best_element = elem

        # Evade penalty: higher evade = harder to hit = worse score
        evade_penalty = (bp.evade + bp.chain_evade) * 0.2

        part_score = type_factor + class_factor + elemental_factor - evade_penalty

        if part_score > best_score:
            best_score = part_score
            best_part_name = bp.name
            best_damage = max(0, type_factor + class_factor + elemental_factor)

            # Build reasoning
            reasons = []
            if dt_defense < 0:
                reasons.append(f"weak to {blade.damage_type} ({dt_defense})")
            elif dt_defense > 0:
                reasons.append(f"resists {blade.damage_type} (+{dt_defense})")
            if best_element and best_element_value > 5:
                reasons.append(f"vulnerable to {best_element} ({best_element_value:+.0f})")
            if class_bonus > 0 and class_key:
                reasons.append(f"{class_key} affinity bonus (+{class_bonus})")
            if bp.evade < 5:
                reasons.append("low evade")
            best_reason = "; ".join(reasons) if reasons else "best overall target"

    return OffenseScore(
        total_score=best_score,
        best_target=best_part_name,
        estimated_damage=best_damage,
        reasoning=best_reason,
    )


def score_defense(
    armor_set: dict[str, tuple[Armor, Material]],
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
) -> DefenseScore:
    """Score an armor set against an enemy's offensive capabilities.

    Considers:
    - Total physical/damage type resistances from all armor pieces + material modifiers
    - Class affinity: armor affinity matching enemy's class
    - Elemental defense: armor elemental affinities vs enemy's likely attack elements
      (inferred from enemy body parts' offensive affinities)
    - Enemy STR -> importance of physical defense
    - Enemy INT -> importance of elemental defense
    """
    if not armor_set:
        return DefenseScore()

    # Aggregate armor stats
    total_physical = 0
    total_blunt = 0
    total_edged = 0
    total_piercing = 0
    total_class_affinity = 0
    total_elemental: dict[str, int] = dict.fromkeys(ELEMENTAL_AFFINITIES, 0)

    class_key = _get_enemy_class_key(enemy.enemy_class)

    for _slot, (armor, material) in armor_set.items():
        # Use shield or armor material modifiers based on type
        if armor.armor_type == "Shield":
            mat_str = material.shield_str
        else:
            mat_str = material.armor_str

        total_physical += armor.physical + mat_str
        total_blunt += armor.blunt
        total_edged += armor.edged
        total_piercing += armor.piercing

        # Class affinity from armor + material
        if class_key:
            armor_class = getattr(armor, class_key, 0)
            mat_class = getattr(material, class_key, 0)
            total_class_affinity += armor_class + mat_class

        # Elemental affinities
        for elem in ELEMENTAL_AFFINITIES:
            armor_elem = getattr(armor, elem, 0)
            mat_elem = getattr(material, elem, 0)
            total_elemental[elem] += armor_elem + mat_elem

    # Infer enemy's primary attack elements from body parts
    # Body parts with high elemental values suggest the enemy uses those elements offensively
    enemy_attack_elements: dict[str, float] = dict.fromkeys(ELEMENTAL_AFFINITIES, 0.0)
    for bp in enemy_body_parts:
        for elem in ELEMENTAL_AFFINITIES:
            bp_elem = getattr(bp, elem, 0)
            # Positive affinity on enemy body part = enemy is strong in that element
            # = they likely use it offensively
            if bp_elem > 0:
                enemy_attack_elements[elem] += bp_elem

    # Physical defense score: weighted by enemy STR
    str_weight = min(enemy.str_stat / 100.0, 2.0)
    avg_damage_type_defense = (total_blunt + total_edged + total_piercing) / 3.0
    phys_score = (total_physical + avg_damage_type_defense) * str_weight

    # Elemental defense score: weighted by enemy INT
    int_weight = min(enemy.int_stat / 100.0, 2.0)
    elem_score = 0.0
    for elem in ELEMENTAL_AFFINITIES:
        # If enemy attacks with this element, our defense in it matters
        attack_strength = enemy_attack_elements[elem]
        if attack_strength > 0:
            elem_score += total_elemental[elem] * (attack_strength / 100.0)
    elem_score *= int_weight

    # Class affinity defense contribution
    class_score = total_class_affinity * 0.5

    total_score = phys_score + elem_score + class_score

    # Estimate damage reduction percentage (heuristic, capped at 80%)
    reduction_pct = min(80.0, max(0.0, total_score / 5.0))

    return DefenseScore(
        total_score=total_score,
        estimated_reduction_pct=reduction_pct,
    )


def _is_grip_compatible(grip: Grip, blade: Blade) -> bool:
    """Check if a grip is compatible with a blade based on compatible_weapons."""
    if not grip.compatible_weapons:
        return False
    compatible = [w.strip() for w in grip.compatible_weapons.split(",")]
    return blade.blade_type in compatible


def optimize_loadout(
    inventory_items: list[InventoryItem],
    enemy: Enemy,
    blades_db: dict[int, Blade],
    grips_db: dict[int, Grip],
    armor_db: dict[int, Armor],
    materials_db: dict[str, Material],
    mode: str = "full",
) -> list[Loadout]:
    """Find the best equipment loadout from inventory to fight a specific enemy.

    Args:
        inventory_items: filtered list of player's inventory items
        enemy: the target enemy (with body_parts loaded)
        blades_db: dict of blade_id -> Blade
        grips_db: dict of grip_id -> Grip
        armor_db: dict of armor_id -> Armor
        materials_db: dict of material_name -> Material
        mode: "full", "offense", or "defense"

    Returns:
        Top 3 loadout results ranked by effectiveness.
    """
    enemy_body_parts = enemy.body_parts

    # Categorize inventory items
    blade_items: list[tuple[InventoryItem, Blade, Material]] = []
    grip_items: list[tuple[InventoryItem, Grip]] = []
    armor_items_by_slot: dict[str, list[tuple[InventoryItem, Armor, Material]]] = {
        slot: [] for slot in ARMOR_TYPE_TO_SLOT.values()
    }

    null_mat = _null_material()

    for inv_item in inventory_items:
        if inv_item.item_type == "blade":
            blade = blades_db.get(inv_item.item_id)
            mat = materials_db.get(inv_item.material) if inv_item.material else null_mat
            if blade:
                blade_items.append((inv_item, blade, mat))
            # Also collect grips attached to blades
            if inv_item.grip_id:
                grip = grips_db.get(inv_item.grip_id)
                if grip:
                    grip_items.append((inv_item, grip))
        elif inv_item.item_type == "armor":
            armor = armor_db.get(inv_item.item_id)
            mat = materials_db.get(inv_item.material) if inv_item.material else null_mat
            if armor:
                slot = ARMOR_TYPE_TO_SLOT.get(armor.armor_type)
                if slot:
                    armor_items_by_slot[slot].append((inv_item, armor, mat))

    # If no grips found from blade items, fall back to checking all grips in DB
    # In practice grips come from the blade's grip_id
    if not grip_items:
        # Use a default grip if none are available
        pass

    results: list[Loadout] = []

    if mode in ("offense", "full"):
        results = _score_offense_combos(blade_items, grip_items, grips_db, enemy, enemy_body_parts)

    if mode == "defense":
        results = _score_defense_combos(armor_items_by_slot, enemy, enemy_body_parts)

    if mode == "full":
        offense_results = results[:10]  # Top 10 offense combos
        defense_results = _score_defense_combos(armor_items_by_slot, enemy, enemy_body_parts)[:10]

        combined: list[Loadout] = []
        for off_loadout in offense_results:
            for def_loadout in defense_results:
                # Check no inventory item ID overlap (can't use same item twice)
                off_ids = {off_loadout.blade_inv_item_id, off_loadout.grip_inv_item_id}
                off_ids.discard(None)
                def_ids = set(def_loadout.armor_inv_item_ids.values())
                if off_ids & def_ids:
                    continue

                # For 1H weapons, shield can be in armor set; for 2H, no shield
                armor_pieces = dict(def_loadout.armor_pieces)
                armor_inv_ids = dict(def_loadout.armor_inv_item_ids)
                if off_loadout.blade and off_loadout.blade.hands == "2H":
                    armor_pieces.pop("shield", None)
                    armor_inv_ids.pop("shield", None)

                combined_score = off_loadout.offense_score * 0.6 + def_loadout.defense_score * 0.4
                combined.append(
                    Loadout(
                        score=combined_score,
                        offense_score=off_loadout.offense_score,
                        defense_score=def_loadout.defense_score,
                        blade=off_loadout.blade,
                        blade_material=off_loadout.blade_material,
                        grip=off_loadout.grip,
                        armor_pieces=armor_pieces,
                        estimated_damage=off_loadout.estimated_damage,
                        target_body_part=off_loadout.target_body_part,
                        target_reason=off_loadout.target_reason,
                        blade_inv_item_id=off_loadout.blade_inv_item_id,
                        grip_inv_item_id=off_loadout.grip_inv_item_id,
                        armor_inv_item_ids=armor_inv_ids,
                    )
                )

        combined.sort(key=lambda x: x.score, reverse=True)
        results = combined

    # Deduplicate: two loadouts are identical if they recommend the same items
    seen: set[tuple] = set()
    unique: list[Loadout] = []
    for loadout in results:
        key = (
            loadout.blade.id if loadout.blade else None,
            loadout.grip.id if loadout.grip else None,
            tuple(sorted(
                (slot, a.id if a else None)
                for slot, (a, _) in loadout.armor_pieces.items()
            )) if loadout.armor_pieces else (),
        )
        if key not in seen:
            seen.add(key)
            unique.append(loadout)

    # Assign ranks and return top 3
    top = unique[:5]
    for i, loadout in enumerate(top, 1):
        loadout.rank = i
    return top


def _score_offense_combos(
    blade_items: list[tuple[InventoryItem, Blade, Material]],
    grip_items: list[tuple[InventoryItem, Grip]],
    grips_db: dict[int, Grip],
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
) -> list[Loadout]:
    """Score all valid blade + grip combinations and return sorted by score."""
    offense_results: list[Loadout] = []

    for inv_item, blade, mat in blade_items:
        # Find compatible grips
        compatible_grips: list[tuple[InventoryItem | None, Grip]] = []

        # First check grips from inventory
        for grip_inv, grip in grip_items:
            if _is_grip_compatible(grip, blade):
                compatible_grips.append((grip_inv, grip))

        # If no inventory grips, check the grip_id on the blade's inventory item
        if not compatible_grips and inv_item.grip_id:
            grip = grips_db.get(inv_item.grip_id)
            if grip and _is_grip_compatible(grip, blade):
                compatible_grips.append((inv_item, grip))

        # If still no compatible grips, use a neutral placeholder score
        if not compatible_grips:
            # Create a minimal grip with zero stats for scoring
            score = score_offense(blade, _null_grip(), mat, enemy, enemy_body_parts)
            offense_results.append(
                Loadout(
                    offense_score=score.total_score,
                    score=score.total_score,
                    blade=blade,
                    blade_material=mat,
                    grip=None,
                    estimated_damage=score.estimated_damage,
                    target_body_part=score.best_target,
                    target_reason=score.reasoning,
                    blade_inv_item_id=inv_item.id,
                )
            )
            continue

        for grip_inv, grip in compatible_grips:
            score = score_offense(blade, grip, mat, enemy, enemy_body_parts)
            # grip_inv might be the same inv_item if the grip is attached to the blade
            grip_inv_id = grip_inv.id if grip_inv and grip_inv.id != inv_item.id else None
            offense_results.append(
                Loadout(
                    offense_score=score.total_score,
                    score=score.total_score,
                    blade=blade,
                    blade_material=mat,
                    grip=grip,
                    estimated_damage=score.estimated_damage,
                    target_body_part=score.best_target,
                    target_reason=score.reasoning,
                    blade_inv_item_id=inv_item.id,
                    grip_inv_item_id=grip_inv_id,
                )
            )

    offense_results.sort(key=lambda x: x.offense_score, reverse=True)
    return offense_results


def _score_defense_combos(
    armor_items_by_slot: dict[str, list[tuple[InventoryItem, Armor, Material]]],
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
) -> list[Loadout]:
    """Score armor combinations and return sorted by defense score.

    To keep computation bounded, we score each slot independently and then
    combine the top picks. For slots with multiple options, we try all
    combinations of the top candidates per slot.
    """
    # For each slot, score pieces individually and keep top 3
    scored_by_slot: dict[str, list[tuple[float, InventoryItem, Armor, Material]]] = {}

    for slot, items in armor_items_by_slot.items():
        slot_scores = []
        for inv_item, armor, mat in items:
            # Score this single piece as a one-piece armor set
            single_set = {slot: (armor, mat)}
            ds = score_defense(single_set, enemy, enemy_body_parts)
            slot_scores.append((ds.total_score, inv_item, armor, mat))
        slot_scores.sort(key=lambda x: x[0], reverse=True)
        scored_by_slot[slot] = slot_scores[:3]

    # Build combinations from slots that have items
    slots_with_items = {slot: pieces for slot, pieces in scored_by_slot.items() if pieces}

    if not slots_with_items:
        return []

    slot_names = list(slots_with_items.keys())
    slot_options = [slots_with_items[s] for s in slot_names]

    defense_results: list[Loadout] = []

    # Limit combinations to avoid combinatorial explosion
    # With max 3 per slot and 6 slots, worst case is 3^6 = 729, which is fine
    for combo in product(*slot_options):
        armor_set: dict[str, tuple[Armor, Material]] = {}
        armor_inv_ids: dict[str, int] = {}
        used_inv_ids: set[int] = set()
        valid = True

        for slot_name, (_, inv_item, armor, mat) in zip(slot_names, combo, strict=True):
            # Ensure no duplicate inventory items
            if inv_item.id in used_inv_ids:
                valid = False
                break
            used_inv_ids.add(inv_item.id)
            armor_set[slot_name] = (armor, mat)
            armor_inv_ids[slot_name] = inv_item.id

        if not valid:
            continue

        ds = score_defense(armor_set, enemy, enemy_body_parts)
        defense_results.append(
            Loadout(
                defense_score=ds.total_score,
                score=ds.total_score,
                armor_pieces=armor_set,
                armor_inv_item_ids=armor_inv_ids,
            )
        )

    defense_results.sort(key=lambda x: x.defense_score, reverse=True)
    return defense_results


def _null_material() -> Material:
    """Create a zero-stat material placeholder for items without a material."""
    return Material(
        id=0,
        name="",
        tier=0,
        str_modifier=0,
        int_modifier=0,
        agi_modifier=0,
        blade_str=0,
        blade_int=0,
        blade_agi=0,
        shield_str=0,
        shield_int=0,
        shield_agi=0,
        armor_str=0,
        armor_int=0,
        armor_agi=0,
        human=0,
        beast=0,
        undead=0,
        phantom=0,
        dragon=0,
        evil=0,
        fire=0,
        water=0,
        wind=0,
        earth=0,
        light=0,
        dark=0,
    )


def _null_grip() -> Grip:
    """Create a zero-stat grip placeholder for scoring blades without a grip."""
    return Grip(
        id=0,
        name="",
        field_name="",
        grip_type="",
        compatible_weapons="",
        str_stat=0,
        int_stat=0,
        agi_stat=0,
        blunt=0,
        edged=0,
        piercing=0,
        gem_slots=0,
        dp=None,
        pp=None,
        game_id=0,
        description_fr="",
        wep_file_id=0,
    )
