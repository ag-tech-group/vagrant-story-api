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
from app.models.gem import Gem
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
class BodyPartScore:
    """Detailed scoring for a single body part target."""

    name: str = ""
    estimated_damage: float = 0.0
    hit_chance: int = 100  # 0-100%
    expected_damage: float = 0.0  # damage * hit_chance / 100
    reasoning: str = ""


@dataclass
class OffenseScore:
    total_score: float = 0.0
    best_target: str = ""
    estimated_damage: float = 0.0
    hit_chance: int = 100
    expected_damage: float = 0.0
    reasoning: str = ""
    body_parts: list[BodyPartScore] = field(default_factory=list)


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
    hit_chance: int = 100
    expected_damage: float = 0.0
    target_body_part: str = ""
    target_reason: str = ""
    body_part_scores: list[BodyPartScore] = field(default_factory=list)
    blade_inv_item_id: int | None = None
    grip_inv_item_id: int | None = None
    armor_inv_item_ids: dict[str, int] = field(default_factory=dict)
    blade_gems: list[Gem] = field(default_factory=list)
    armor_gems: dict[str, list[Gem]] = field(default_factory=dict)

    def compute_combined_stats(self) -> dict[str, int | str]:
        """Compute combined player stats from this loadout's equipment."""
        totals: dict[str, int] = {
            "str": 0,
            "int": 0,
            "agi": 0,
            "human": 0,
            "beast": 0,
            "undead": 0,
            "phantom": 0,
            "dragon": 0,
            "evil": 0,
            "physical": 0,
            "fire": 0,
            "water": 0,
            "wind": 0,
            "earth": 0,
            "light": 0,
            "dark": 0,
        }
        range_val = 0
        risk_val = 0
        damage_type = ""
        blunt = 0
        edged = 0
        piercing = 0

        if self.blade:
            mat = self.blade_material
            totals["str"] += self.blade.str_stat + (mat.blade_str if mat else 0)
            totals["int"] += self.blade.int_stat + (mat.blade_int if mat else 0)
            totals["agi"] += self.blade.agi_stat + (mat.blade_agi if mat else 0)
            range_val = self.blade.range_stat
            risk_val = self.blade.risk
            damage_type = self.blade.damage_type
            if mat:
                for key in ELEMENTAL_AFFINITIES:
                    totals[key] += getattr(mat, key, 0)
                for key in CLASS_AFFINITIES:
                    totals[key] += getattr(mat, key, 0)
            for gem in self.blade_gems:
                totals["str"] += gem.str_stat
                totals["int"] += gem.int_stat
                totals["agi"] += gem.agi_stat
                totals["physical"] += gem.physical
                for key in ELEMENTAL_AFFINITIES:
                    totals[key] += getattr(gem, key, 0)
                for key in CLASS_AFFINITIES:
                    totals[key] += getattr(gem, key, 0)

        if self.grip:
            totals["str"] += self.grip.str_stat
            totals["int"] += self.grip.int_stat
            totals["agi"] += self.grip.agi_stat
            blunt = self.grip.blunt
            edged = self.grip.edged
            piercing = self.grip.piercing

        for _slot, (armor_item, mat) in self.armor_pieces.items():
            is_shield = armor_item.armor_type == "Shield"
            is_accessory = armor_item.armor_type == "Accessory"
            if is_accessory:
                totals["str"] += armor_item.str_stat
                totals["int"] += armor_item.int_stat
                totals["agi"] += armor_item.agi_stat
            elif is_shield:
                totals["str"] += armor_item.str_stat + (mat.shield_str if mat else 0)
                totals["int"] += armor_item.int_stat + (mat.shield_int if mat else 0)
                totals["agi"] += armor_item.agi_stat + (mat.shield_agi if mat else 0)
            else:
                totals["str"] += armor_item.str_stat + (mat.armor_str if mat else 0)
                totals["int"] += armor_item.int_stat + (mat.armor_int if mat else 0)
                totals["agi"] += armor_item.agi_stat + (mat.armor_agi if mat else 0)
            if mat and not is_accessory:
                for key in ELEMENTAL_AFFINITIES:
                    totals[key] += getattr(mat, key, 0)
                for key in CLASS_AFFINITIES:
                    totals[key] += getattr(mat, key, 0)
            for gem in self.armor_gems.get(_slot, []):
                totals["str"] += gem.str_stat
                totals["int"] += gem.int_stat
                totals["agi"] += gem.agi_stat
                totals["physical"] += gem.physical
                for key in ELEMENTAL_AFFINITIES:
                    totals[key] += getattr(gem, key, 0)
                for key in CLASS_AFFINITIES:
                    totals[key] += getattr(gem, key, 0)

        return {
            **totals,
            "range": range_val,
            "risk": risk_val,
            "damage_type": damage_type,
            "blunt": blunt,
            "edged": edged,
            "piercing": piercing,
        }


def _get_enemy_class_key(enemy_class: str) -> str | None:
    """Map enemy_class string to the affinity column name."""
    lower = enemy_class.lower()
    for key in CLASS_AFFINITIES:
        if key in lower:
            return key
    return None


def _get_bp_elemental(bp: EnemyBodyPart, elem: str) -> int:
    """Get a body part's elemental defense, mapping 'wind' -> 'air' column."""
    col = "air" if elem == "wind" else elem
    return getattr(bp, col, 0)


def score_offense(
    blade: Blade,
    grip: Grip,
    material: Material,
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
    gems: list[Gem] | None = None,
    accessory: Armor | None = None,
    player_str: int = 0,
    player_agi: int = 0,
    blade_pp_pct: int = 100,
    blade_dp_pct: int = 0,
) -> OffenseScore:
    """Score a weapon setup against an enemy using the real VS damage formula.

    Uses the actual Vagrant Story combat mechanics:
      Attack = (STR + WeapSTR + AccSTR) * (100 + Modifier) / 100
      Modifier = (WeapClass + AccClass + WeapAffinity + AccAffinity
                  + WeapType + AccType + PP% - DP%) // 4
      Damage = Attack - Defense

    Reference: Beamup's Combat Mechanics Guide (GameFAQs)
    """
    if not enemy_body_parts:
        return OffenseScore(reasoning="Enemy has no body parts to target")

    blade_gems = gems or []

    # ── Player's total STR (base + weapon + accessory) ──────────────
    weap_str = blade.str_stat + grip.str_stat + material.blade_str
    weap_str += sum(g.str_stat for g in blade_gems)
    acc_str = accessory.str_stat if accessory else 0
    total_str = player_str + weap_str + acc_str

    # ── Player's total AGI (base + weapon + accessory + armor) ──────
    weap_agi = blade.agi_stat + grip.agi_stat + material.blade_agi
    weap_agi += sum(g.agi_stat for g in blade_gems)
    acc_agi = accessory.agi_stat if accessory else 0
    total_agi = player_agi + weap_agi + acc_agi

    # ── Weapon Class affinity (vs enemy class) ──────────────────────
    class_key = _get_enemy_class_key(enemy.enemy_class)
    weap_class = getattr(material, class_key, 0) if class_key else 0
    weap_class += sum(getattr(g, class_key, 0) for g in blade_gems)
    acc_class = getattr(accessory, class_key, 0) if accessory and class_key else 0

    # ── Weapon Type (grip's stat matching blade's damage type) ──────
    damage_type_key = blade.damage_type.lower()
    weap_type = getattr(grip, damage_type_key, 0) if damage_type_key in DAMAGE_TYPES else 0
    acc_type = 0  # accessories don't have damage type stats

    # ── Score each body part ────────────────────────────────────────
    bp_scores: list[BodyPartScore] = []

    for bp in enemy_body_parts:
        # Weapon Affinity: best elemental match (material + gems vs body part weakness)
        # In VS, the elemental affinity used is the weapon's elemental that the
        # body part is weakest to (most negative defense = biggest bonus for attacker)
        weap_affinity = 0
        acc_affinity = 0
        best_element = ""
        for elem in ELEMENTAL_AFFINITIES:
            mat_elem = getattr(material, elem, 0)
            gem_elem = sum(getattr(g, elem, 0) for g in blade_gems)
            weapon_elem_total = mat_elem + gem_elem
            if weapon_elem_total > weap_affinity:
                weap_affinity = weapon_elem_total
                best_element = elem

        # Attack modifier: (Class + Affinity + Type + PP% - DP%) / 4
        attack_modifier = (
            weap_class
            + acc_class
            + weap_affinity
            + acc_affinity
            + weap_type
            + acc_type
            + blade_pp_pct
            - blade_dp_pct
        ) // 4

        # Attack value
        attack = total_str * (100 + attack_modifier) // 100

        # Enemy Defense for this body part
        # Defense modifier comes from body part's type + physical + elemental resistances
        bp_type = getattr(bp, damage_type_key, 0) if damage_type_key in DAMAGE_TYPES else 0
        bp_physical = bp.physical

        # Best elemental defense the enemy has (matching our weapon's affinity)
        bp_affinity = _get_bp_elemental(bp, best_element) if best_element else 0

        # Enemy class defense (enemies have inherent class — they don't have "class" stats
        # in the same way, so we use the body part physical as the main defense base)
        enemy_def_modifier = (bp_type + bp_physical + bp_affinity) // 4

        # Enemy base defense: (EnemySTR - 20) * (100 + modifier) / 100
        enemy_defense = max(0, (enemy.str_stat - 20) * (100 + enemy_def_modifier) // 100)

        # Estimated damage (regular attack, multiplier = 1.0)
        est_damage = max(0, attack - enemy_defense)

        # Hit chance: Hit% = 100 + Acc - Dge (assume RISK = 0 for both sides)
        acc = total_agi  # floor(AGL * (100-0) / 100) = AGL
        dge = enemy.agi_stat + bp.evade  # floor((AGL + EVA) * (100-0) / 100)
        hit_pct = max(5, min(100, 100 + acc - dge))

        # Expected damage (hit-chance weighted)
        expected = est_damage * hit_pct / 100.0

        # Build reasoning
        reasons = []
        if bp_type < 0:
            reasons.append(f"weak to {blade.damage_type} ({bp_type})")
        elif bp_type > 10:
            reasons.append(f"resists {blade.damage_type} (+{bp_type})")
        if weap_affinity > 5 and best_element:
            reasons.append(f"{best_element} affinity (+{weap_affinity})")
        if class_key and weap_class > 5:
            reasons.append(f"{class_key} affinity bonus (+{weap_class})")
        if bp.evade > 10:
            reasons.append(f"high evade ({bp.evade})")
        elif bp.evade == 0:
            reasons.append("low evade")

        bp_scores.append(
            BodyPartScore(
                name=bp.name,
                estimated_damage=round(est_damage, 1),
                hit_chance=hit_pct,
                expected_damage=round(expected, 1),
                reasoning="; ".join(reasons) if reasons else "no special modifiers",
            )
        )

    # Sort by expected damage (hit-chance weighted) — primary ranking metric
    bp_scores.sort(key=lambda x: x.expected_damage, reverse=True)

    best = bp_scores[0] if bp_scores else BodyPartScore()

    return OffenseScore(
        total_score=best.expected_damage,
        best_target=best.name,
        estimated_damage=best.estimated_damage,
        hit_chance=best.hit_chance,
        expected_damage=best.expected_damage,
        reasoning=best.reasoning,
        body_parts=bp_scores,
    )


def score_defense(
    armor_set: dict[str, tuple[Armor, Material]],
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
    armor_gems: dict[str, list[Gem]] | None = None,
) -> DefenseScore:
    """Score an armor set against an enemy's offensive capabilities.

    Considers:
    - Total physical/damage type resistances from all armor pieces + material modifiers
    - Class affinity: armor affinity matching enemy's class
    - Elemental defense: armor elemental affinities vs enemy's likely attack elements
      (inferred from enemy body parts' offensive affinities)
    - Gem stats from armor pieces (class, elemental, physical)
    - Enemy STR -> importance of physical defense
    - Enemy INT -> importance of elemental defense
    """
    if not armor_set:
        return DefenseScore()

    slot_gems = armor_gems or {}

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

        # Gem contributions for this armor slot
        for gem in slot_gems.get(_slot, []):
            total_physical += gem.physical
            if class_key:
                total_class_affinity += getattr(gem, class_key, 0)
            for elem in ELEMENTAL_AFFINITIES:
                total_elemental[elem] += getattr(gem, elem, 0)

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
    compatible = [w.strip() for w in grip.compatible_weapons.split("/")]
    return blade.blade_type in compatible


def _resolve_gems(inv_item: InventoryItem, gems_db: dict[int, Gem]) -> list[Gem]:
    """Collect the Gem objects attached to an inventory item."""
    result: list[Gem] = []
    for gem_id in (inv_item.gem_1_id, inv_item.gem_2_id, inv_item.gem_3_id):
        if gem_id is not None:
            gem = gems_db.get(gem_id)
            if gem:
                result.append(gem)
    return result


def optimize_loadout(
    inventory_items: list[InventoryItem],
    enemy: Enemy,
    blades_db: dict[int, Blade],
    grips_db: dict[int, Grip],
    armor_db: dict[int, Armor],
    materials_db: dict[str, Material],
    gems_db: dict[int, Gem] | None = None,
    mode: str = "full",
    include_2h: bool = True,
    player_str: int = 0,
    player_int: int = 0,
    player_agi: int = 0,
) -> list[Loadout]:
    """Find the best equipment loadout from inventory to fight a specific enemy.

    Uses the real Vagrant Story damage formula for scoring. Player base stats
    are optional — if provided (from save import or API request), the damage
    estimates will be much more accurate.

    Args:
        inventory_items: filtered list of player's inventory items
        enemy: the target enemy (with body_parts loaded)
        blades_db: dict of blade_id -> Blade
        grips_db: dict of grip_id -> Grip
        armor_db: dict of armor_id -> Armor
        materials_db: dict of material_name -> Material
        gems_db: dict of gem_id -> Gem (optional)
        mode: "full", "offense", or "defense"
        include_2h: whether to include 2H weapons in offense/full results
        player_str: Ashley's base STR (0 if unknown)
        player_int: Ashley's base INT (0 if unknown)
        player_agi: Ashley's base AGI (0 if unknown)

    Returns:
        Top 5 loadout results ranked by effectiveness.
    """
    gems_lookup = gems_db or {}
    enemy_body_parts = enemy.body_parts

    # Categorize inventory items (with gem lists)
    blade_items: list[tuple[InventoryItem, Blade, Material, list[Gem]]] = []
    grip_items: list[tuple[InventoryItem, Grip]] = []
    armor_items_by_slot: dict[str, list[tuple[InventoryItem, Armor, Material, list[Gem]]]] = {
        slot: [] for slot in ARMOR_TYPE_TO_SLOT.values()
    }

    null_mat = _null_material()

    for inv_item in inventory_items:
        if inv_item.item_type == "blade":
            blade = blades_db.get(inv_item.item_id)
            mat = materials_db.get(inv_item.material) if inv_item.material else null_mat
            if blade:
                if not include_2h and blade.hands == "2H":
                    continue
                item_gems = _resolve_gems(inv_item, gems_lookup)
                blade_items.append((inv_item, blade, mat, item_gems))
            # Also collect grips attached to blades
            if inv_item.grip_id:
                grip = grips_db.get(inv_item.grip_id)
                if grip:
                    grip_items.append((inv_item, grip))
        elif inv_item.item_type == "grip":
            grip = grips_db.get(inv_item.item_id)
            if grip:
                grip_items.append((inv_item, grip))
        elif inv_item.item_type == "armor":
            armor = armor_db.get(inv_item.item_id)
            mat = materials_db.get(inv_item.material) if inv_item.material else null_mat
            if armor:
                slot = ARMOR_TYPE_TO_SLOT.get(armor.armor_type)
                if slot:
                    item_gems = _resolve_gems(inv_item, gems_lookup)
                    armor_items_by_slot[slot].append((inv_item, armor, mat, item_gems))

    # Extract the equipped accessory for offense scoring
    equipped_accessory: Armor | None = None
    for inv_item, armor, _mat, _gems in armor_items_by_slot.get("accessory", []):
        if inv_item.equip_slot == "accessory":
            equipped_accessory = armor
            break

    results: list[Loadout] = []

    if mode in ("offense", "full"):
        results = _score_offense_combos(
            blade_items,
            grip_items,
            grips_db,
            enemy,
            enemy_body_parts,
            accessory=equipped_accessory,
            player_str=player_str,
            player_agi=player_agi,
        )

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
                def_armor_gems = dict(def_loadout.armor_gems)
                if off_loadout.blade and off_loadout.blade.hands == "2H":
                    armor_pieces.pop("shield", None)
                    armor_inv_ids.pop("shield", None)
                    def_armor_gems.pop("shield", None)

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
                        hit_chance=off_loadout.hit_chance,
                        expected_damage=off_loadout.expected_damage,
                        target_body_part=off_loadout.target_body_part,
                        target_reason=off_loadout.target_reason,
                        body_part_scores=off_loadout.body_part_scores,
                        blade_inv_item_id=off_loadout.blade_inv_item_id,
                        grip_inv_item_id=off_loadout.grip_inv_item_id,
                        armor_inv_item_ids=armor_inv_ids,
                        blade_gems=off_loadout.blade_gems,
                        armor_gems=def_armor_gems,
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
            tuple(
                sorted((slot, a.id if a else None) for slot, (a, _) in loadout.armor_pieces.items())
            )
            if loadout.armor_pieces
            else (),
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
    blade_items: list[tuple[InventoryItem, Blade, Material, list[Gem]]],
    grip_items: list[tuple[InventoryItem, Grip]],
    grips_db: dict[int, Grip],
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
    accessory: Armor | None = None,
    player_str: int = 0,
    player_agi: int = 0,
) -> list[Loadout]:
    """Score all valid blade + grip combinations and return sorted by expected damage."""
    offense_results: list[Loadout] = []

    def _score_and_append(
        inv_item: InventoryItem,
        blade: Blade,
        mat: Material,
        grip: Grip | None,
        blade_gems: list[Gem],
        grip_inv_id: int | None,
    ) -> None:
        # Calculate PP%/DP% from inventory item if available
        pp_pct = 100
        dp_pct = 0
        if inv_item.pp_max and inv_item.pp_max > 0:
            pp_pct = 100 * (inv_item.pp_current or 0) // inv_item.pp_max
        if inv_item.dp_max and inv_item.dp_max > 0:
            dp_pct = 100 * (inv_item.dp_max - (inv_item.dp_current or 0)) // inv_item.dp_max

        score = score_offense(
            blade,
            grip or _null_grip(),
            mat,
            enemy,
            enemy_body_parts,
            gems=blade_gems,
            accessory=accessory,
            player_str=player_str,
            player_agi=player_agi,
            blade_pp_pct=pp_pct,
            blade_dp_pct=dp_pct,
        )
        offense_results.append(
            Loadout(
                offense_score=score.total_score,
                score=score.total_score,
                blade=blade,
                blade_material=mat,
                grip=grip,
                estimated_damage=score.estimated_damage,
                hit_chance=score.hit_chance,
                expected_damage=score.expected_damage,
                target_body_part=score.best_target,
                target_reason=score.reasoning,
                body_part_scores=score.body_parts,
                blade_inv_item_id=inv_item.id,
                grip_inv_item_id=grip_inv_id,
                blade_gems=blade_gems,
            )
        )

    for inv_item, blade, mat, blade_gems in blade_items:
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

        # If still no compatible grips, score without grip
        if not compatible_grips:
            _score_and_append(inv_item, blade, mat, None, blade_gems, None)
            continue

        for grip_inv, grip in compatible_grips:
            grip_inv_id = grip_inv.id if grip_inv and grip_inv.id != inv_item.id else None
            _score_and_append(inv_item, blade, mat, grip, blade_gems, grip_inv_id)

    offense_results.sort(key=lambda x: x.offense_score, reverse=True)
    return offense_results


def _score_defense_combos(
    armor_items_by_slot: dict[str, list[tuple[InventoryItem, Armor, Material, list[Gem]]]],
    enemy: Enemy,
    enemy_body_parts: list[EnemyBodyPart],
) -> list[Loadout]:
    """Score armor combinations and return sorted by defense score.

    To keep computation bounded, we score each slot independently and then
    combine the top picks. For slots with multiple options, we try all
    combinations of the top candidates per slot.
    """
    # For each slot, score pieces individually and keep top 3
    scored_by_slot: dict[str, list[tuple[float, InventoryItem, Armor, Material, list[Gem]]]] = {}

    for slot, items in armor_items_by_slot.items():
        slot_scores: list[tuple[float, InventoryItem, Armor, Material, list[Gem]]] = []
        for inv_item, armor, mat, item_gems in items:
            # Score this single piece as a one-piece armor set
            single_set = {slot: (armor, mat)}
            single_gems = {slot: item_gems} if item_gems else {}
            ds = score_defense(single_set, enemy, enemy_body_parts, armor_gems=single_gems)
            slot_scores.append((ds.total_score, inv_item, armor, mat, item_gems))
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
        combo_armor_gems: dict[str, list[Gem]] = {}
        used_inv_ids: set[int] = set()
        valid = True

        for slot_name, (_, inv_item, armor, mat, item_gems) in zip(slot_names, combo, strict=True):
            # Ensure no duplicate inventory items
            if inv_item.id in used_inv_ids:
                valid = False
                break
            used_inv_ids.add(inv_item.id)
            armor_set[slot_name] = (armor, mat)
            armor_inv_ids[slot_name] = inv_item.id
            if item_gems:
                combo_armor_gems[slot_name] = item_gems

        if not valid:
            continue

        ds = score_defense(armor_set, enemy, enemy_body_parts, armor_gems=combo_armor_gems)
        defense_results.append(
            Loadout(
                defense_score=ds.total_score,
                score=ds.total_score,
                armor_pieces=armor_set,
                armor_inv_item_ids=armor_inv_ids,
                armor_gems=combo_armor_gems,
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
