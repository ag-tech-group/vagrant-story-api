"""Unit tests for the loadout scoring formulas.

These tests construct stub SQLAlchemy model instances (no DB) so they can
verify the attack/defense arithmetic in isolation. They pin the behavior that
was previously broken: Class/Affinity/Type modifiers must have four times the
weight on Defense as on Attack, and the body part's ``physical`` column must
be used as the defender's affinity rating when the attacker has no elemental.
"""

from __future__ import annotations

import pytest

from app.models.blade import Blade
from app.models.enemy import Enemy, EnemyBodyPart
from app.models.grip import Grip
from app.models.material import Material
from app.services.loadout_scorer import score_offense

# ── Helpers ──────────────────────────────────────────────────────────


_MATERIAL_INT_FIELDS = (
    "str_modifier",
    "int_modifier",
    "agi_modifier",
    "blade_str",
    "blade_int",
    "blade_agi",
    "shield_str",
    "shield_int",
    "shield_agi",
    "armor_str",
    "armor_int",
    "armor_agi",
    "human",
    "beast",
    "undead",
    "phantom",
    "dragon",
    "evil",
    "fire",
    "water",
    "wind",
    "earth",
    "light",
    "dark",
)


def _material(name: str, **overrides: int) -> Material:
    kwargs = dict.fromkeys(_MATERIAL_INT_FIELDS, 0)
    kwargs.update(overrides)
    return Material(name=name, tier=1, **kwargs)


def _blade(name: str, str_stat: int, damage_type: str, blade_type: str = "Sword") -> Blade:
    return Blade(
        game_id=1,
        field_name=name.replace(" ", "_"),
        name=name,
        blade_type=blade_type,
        damage_type=damage_type,
        risk=1,
        str_stat=str_stat,
        int_stat=0,
        agi_stat=-1,
        range_stat=3,
        damage=2,
        hands="1H",
    )


def _grip(
    name: str,
    compatible: str,
    *,
    blunt: int = 0,
    edged: int = 0,
    piercing: int = 0,
    str_stat: int = 1,
    agi_stat: int = -1,
) -> Grip:
    return Grip(
        game_id=1,
        field_name=name.replace(" ", "_"),
        name=name,
        grip_type=compatible.split("/")[0],
        compatible_weapons=compatible,
        str_stat=str_stat,
        int_stat=0,
        agi_stat=agi_stat,
        blunt=blunt,
        edged=edged,
        piercing=piercing,
        gem_slots=0,
        dp=None,
        pp=None,
        wep_file_id=0,
    )


def _body_part(
    name: str, physical: int, blunt: int, edged: int, piercing: int, evade: int
) -> EnemyBodyPart:
    # Use placeholder elemental values that match the real Golem (all resist).
    return EnemyBodyPart(
        name=name,
        physical=physical,
        air=18,
        fire=72,
        water=45,
        earth=75,
        light=72,
        dark=55,
        blunt=blunt,
        edged=edged,
        piercing=piercing,
        evade=evade,
        chain_evade=0,
    )


# ── Golem fixture (matches data/enemies.json) ────────────────────────


@pytest.fixture
def golem() -> Enemy:
    return Enemy(
        name="Golem",
        enemy_class="Evil",
        hp=240,
        mp=15,
        str_stat=125,
        int_stat=118,
        agi_stat=92,
        movement=6,
        is_boss=False,
    )


@pytest.fixture
def golem_body_parts() -> list[EnemyBodyPart]:
    return [
        _body_part("R. Arm", 32, blunt=-15, edged=5, piercing=15, evade=15),
        _body_part("L. Arm", 32, blunt=-15, edged=5, piercing=15, evade=15),
        _body_part("Head", 32, blunt=-18, edged=2, piercing=11, evade=52),
        _body_part("Body", 32, blunt=-30, edged=-5, piercing=0, evade=48),
        _body_part("R. Leg", 32, blunt=-10, edged=5, piercing=15, evade=0),
        _body_part("L. Leg", 32, blunt=-10, edged=5, piercing=15, evade=0),
    ]


@pytest.fixture
def iron() -> Material:
    # Iron from data/materials.json — no positive elemental affinities.
    return _material(
        "Iron",
        human=-2,
        beast=1,
        undead=1,
        phantom=0,
        dragon=10,
        evil=0,
        fire=-4,
        water=-4,
        wind=0,
        earth=-1,
        light=0,
        dark=0,
    )


# ── Tests ────────────────────────────────────────────────────────────


class TestGolemDamageTypeWeakness:
    """Regression tests for the user-reported issue where the optimizer
    recommended an Edged weapon against a Blunt-weak Golem.

    Golem's body parts range from −10 (legs) to −30 (body) blunt, versus
    −5 to +5 edged. Blunt should decisively outrank edged on every body
    part and therefore in the overall best-target score.
    """

    def test_goblin_club_outdamages_scimitar_per_body_part(
        self, golem: Enemy, golem_body_parts: list[EnemyBodyPart], iron: Material
    ):
        scimitar = _blade("Scimitar", str_stat=7, damage_type="Edged", blade_type="Sword")
        short_hilt = _grip("Short Hilt", "Dagger/Sword/Great Sword", edged=4, piercing=1)

        goblin_club = _blade(
            "Goblin Club", str_stat=6, damage_type="Blunt", blade_type="Axe / Mace"
        )
        wooden_grip = _grip(
            "Wooden Grip", "Axe/Mace/Great Axe/Heavy Mace/Staff", blunt=5, edged=1, agi_stat=-2
        )

        # Use a non-zero player_str so the formulas produce non-saturated
        # numbers we can compare. 120 is roughly the user's reported case.
        kwargs = {
            "enemy": golem,
            "enemy_body_parts": golem_body_parts,
            "accessory": None,
            "player_str": 120,
            "player_agi": 30,
            "blade_pp_pct": 100,
            "blade_dp_pct": 0,
        }
        edged = score_offense(scimitar, short_hilt, iron, **kwargs)
        blunt = score_offense(goblin_club, wooden_grip, iron, **kwargs)

        # Assertion 1: overall expected damage clearly favors blunt.
        assert blunt.expected_damage > edged.expected_damage * 1.5, (
            f"blunt ({blunt.expected_damage}) should beat edged ({edged.expected_damage}) "
            f"by at least 1.5x against a Blunt-weak Golem"
        )

        # Assertion 2: per-body-part raw damage favors blunt on every part
        # that the damage-type weakness applies to. Match on part name so
        # the comparison is order-independent.
        edged_by_name = {bp.name: bp for bp in edged.body_parts}
        blunt_by_name = {bp.name: bp for bp in blunt.body_parts}
        for name in edged_by_name:
            edged_bp = edged_by_name[name]
            blunt_bp = blunt_by_name[name]
            assert blunt_bp.estimated_damage >= edged_bp.estimated_damage, (
                f"{name}: blunt {blunt_bp.estimated_damage} should be >= "
                f"edged {edged_bp.estimated_damage}"
            )
        # Body takes the biggest hit from blunt (−30 vs −5 edged) — assert a
        # meaningful per-hit gap there specifically.
        assert blunt_by_name["Body"].estimated_damage > edged_by_name["Body"].estimated_damage + 15

    def test_optimizer_picks_lowest_evade_target(
        self, golem: Enemy, golem_body_parts: list[EnemyBodyPart], iron: Material
    ):
        """The best_target should be chosen by expected damage, not raw
        damage. Golem's Body has the highest raw damage for blunt but 48
        evade, while the Legs have 0 evade — so Legs should win on expected.
        """
        goblin_club = _blade(
            "Goblin Club", str_stat=6, damage_type="Blunt", blade_type="Axe / Mace"
        )
        wooden_grip = _grip(
            "Wooden Grip", "Axe/Mace/Great Axe/Heavy Mace/Staff", blunt=5, edged=1, agi_stat=-2
        )

        result = score_offense(
            goblin_club,
            wooden_grip,
            iron,
            golem,
            golem_body_parts,
            player_str=120,
            player_agi=30,
        )
        assert result.best_target in ("R. Leg", "L. Leg")


class TestAttackDefenseFormula:
    """Pin the structural fixes to the attack/defense formula."""

    def test_defense_modifier_uses_physical_column_for_default_affinity(
        self, golem: Enemy, iron: Material
    ):
        """With no gems, the weapon's affinity is Physical — so the body
        part's ``physical`` column must drive the defense modifier. Doubling
        the physical rating must raise enemy defense and lower damage.
        """
        scimitar = _blade("Scimitar", str_stat=7, damage_type="Edged")
        short_hilt = _grip("Short Hilt", "Dagger/Sword/Great Sword", edged=4)

        base = [_body_part("Body", physical=32, blunt=0, edged=0, piercing=0, evade=0)]
        tougher = [_body_part("Body", physical=64, blunt=0, edged=0, piercing=0, evade=0)]

        kwargs = {
            "blade": scimitar,
            "grip": short_hilt,
            "material": iron,
            "enemy": golem,
            "player_str": 120,
            "player_agi": 30,
        }
        base_result = score_offense(enemy_body_parts=base, **kwargs)
        tougher_result = score_offense(enemy_body_parts=tougher, **kwargs)

        assert tougher_result.estimated_damage < base_result.estimated_damage, (
            "doubling the body part's physical rating should reduce damage, "
            "proving bp.physical is being applied as the defense modifier"
        )

    def test_damage_type_weakness_has_four_times_attack_weight(self, golem: Enemy, iron: Material):
        """A +20 body-part damage-type rating (resist) should change damage
        more than a +20 grip damage-type rating (attack bonus). The game's
        real formula gives Class/Affinity/Type four times the weight on
        Defense as on Attack — this test pins that asymmetry.
        """
        scimitar = _blade("Scimitar", str_stat=7, damage_type="Edged")

        weak_grip = _grip("Weak", "Dagger/Sword/Great Sword", edged=0)
        strong_grip = _grip("Strong", "Dagger/Sword/Great Sword", edged=20)

        resistant_bp = [_body_part("Body", physical=0, blunt=0, edged=20, piercing=0, evade=0)]
        neutral_bp = [_body_part("Body", physical=0, blunt=0, edged=0, piercing=0, evade=0)]

        # Case A: weaker weapon vs neutral defender.
        attack_bonus = score_offense(
            scimitar,
            strong_grip,
            iron,
            golem,
            neutral_bp,
            player_str=120,
            player_agi=30,
        )
        baseline = score_offense(
            scimitar,
            weak_grip,
            iron,
            golem,
            neutral_bp,
            player_str=120,
            player_agi=30,
        )
        # Case B: same neutral weapon vs resistant defender (+20 edged).
        defense_resist = score_offense(
            scimitar,
            weak_grip,
            iron,
            golem,
            resistant_bp,
            player_str=120,
            player_agi=30,
        )

        attack_gain = attack_bonus.estimated_damage - baseline.estimated_damage
        defense_loss = baseline.estimated_damage - defense_resist.estimated_damage

        # Defense impact should be several times attack impact for the same
        # point value. Exact ratio depends on int truncation; 2x is a safe
        # floor that still proves the formula is no longer symmetric.
        assert defense_loss >= attack_gain * 2, (
            f"+20 edged on defender should lower damage more than +20 edged on grip "
            f"raises it (defense_loss={defense_loss}, attack_gain={attack_gain})"
        )


class TestEmptyAndEdgeCases:
    def test_empty_body_parts_returns_reason(self, golem: Enemy, iron: Material):
        scimitar = _blade("Scimitar", str_stat=7, damage_type="Edged")
        short_hilt = _grip("Short Hilt", "Dagger/Sword/Great Sword", edged=4)

        result = score_offense(scimitar, short_hilt, iron, golem, [], player_str=120, player_agi=30)
        assert result.estimated_damage == 0
        assert "no body parts" in result.reasoning.lower()

    def test_damage_never_goes_negative(self, golem: Enemy, iron: Material):
        """A weak player versus a tough enemy must floor at 0, not a negative."""
        scimitar = _blade("Scimitar", str_stat=7, damage_type="Edged")
        short_hilt = _grip("Short Hilt", "Dagger/Sword/Great Sword", edged=4)
        bp = [_body_part("Body", physical=100, blunt=0, edged=100, piercing=0, evade=0)]

        result = score_offense(scimitar, short_hilt, iron, golem, bp, player_str=0, player_agi=0)
        for part in result.body_parts:
            assert part.estimated_damage >= 0
