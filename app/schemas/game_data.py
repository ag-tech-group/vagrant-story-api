from datetime import datetime

from pydantic import BaseModel, Field

# ── Area / Room schemas ────────────────────────────────────────────


class RoomRead(BaseModel):
    id: int
    name: str
    area_id: int
    area_name: str = ""

    model_config = {"from_attributes": True}


class RoomDetailRead(BaseModel):
    id: int
    name: str
    area_id: int
    area_name: str = ""

    model_config = {"from_attributes": True}


class AreaRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class AreaDetailRead(BaseModel):
    id: int
    name: str
    rooms: list[RoomRead] = []

    model_config = {"from_attributes": True}


class BladeRead(BaseModel):
    id: int
    game_id: int
    field_name: str
    name: str
    description_fr: str
    wep_file_id: int
    blade_type: str
    damage_type: str
    risk: int
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    agi_stat: int = Field(serialization_alias="agi")
    range_stat: int = Field(serialization_alias="range")
    damage: int
    hands: str = "1H"

    model_config = {"from_attributes": True, "populate_by_name": True}


class GripRead(BaseModel):
    id: int
    game_id: int
    field_name: str
    name: str
    description_fr: str
    wep_file_id: int
    grip_type: str = ""
    compatible_weapons: str = ""
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    agi_stat: int = Field(serialization_alias="agi")
    blunt: int = 0
    edged: int = 0
    piercing: int = 0
    gem_slots: int = 0
    dp: int | None = None
    pp: int | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class ArmorRead(BaseModel):
    id: int
    game_id: int
    field_name: str
    name: str
    description_fr: str
    wep_file_id: int
    armor_type: str
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    agi_stat: int = Field(serialization_alias="agi")
    gem_slots: int
    human: int = 0
    beast: int = 0
    undead: int = 0
    phantom: int = 0
    dragon: int = 0
    evil: int = 0
    fire: int = 0
    water: int = 0
    wind: int = 0
    earth: int = 0
    light: int = 0
    dark: int = 0
    blunt: int = 0
    edged: int = 0
    piercing: int = 0
    physical: int = 0

    model_config = {"from_attributes": True, "populate_by_name": True}


class GemRead(BaseModel):
    id: int
    game_id: int
    field_name: str
    name: str
    description_fr: str
    description: str = ""
    magnitude: str
    affinity_type: str
    gem_type: str = ""
    str_stat: int = Field(0, serialization_alias="str")
    int_stat: int = Field(0, serialization_alias="int")
    agi_stat: int = Field(0, serialization_alias="agi")
    human: int = 0
    beast: int = 0
    undead: int = 0
    phantom: int = 0
    dragon: int = 0
    evil: int = 0
    physical: int = 0
    fire: int = 0
    water: int = 0
    wind: int = 0
    earth: int = 0
    light: int = 0
    dark: int = 0

    model_config = {"from_attributes": True, "populate_by_name": True}


class MaterialRead(BaseModel):
    id: int
    name: str
    tier: int
    str_modifier: int
    int_modifier: int
    agi_modifier: int
    blade_str: int = 0
    blade_int: int = 0
    blade_agi: int = 0
    shield_str: int = 0
    shield_int: int = 0
    shield_agi: int = 0
    armor_str: int = 0
    armor_int: int = 0
    armor_agi: int = 0
    human: int
    beast: int
    undead: int
    phantom: int
    dragon: int
    evil: int
    fire: int
    water: int
    wind: int
    earth: int
    light: int
    dark: int

    model_config = {"from_attributes": True}


class ConsumableRead(BaseModel):
    id: int
    game_id: int
    field_name: str
    name: str
    description_fr: str
    description: str = ""
    effects: list | dict | None = None
    hp_restore: str = ""
    mp_restore: str = ""
    risk_reduce: str = ""
    status_cure: str = ""
    permanent_stat: str = ""
    drop_rate: str = ""
    drop_location: str = ""

    model_config = {"from_attributes": True}


class SpellRead(BaseModel):
    id: int
    name: str
    category: str
    mp_cost: str = ""
    targeting: str = ""
    affinity: str = ""
    effect: str = ""
    grimoire: str = ""

    model_config = {"from_attributes": True}


class KeyRead(BaseModel):
    id: int
    name: str
    area: str = ""
    room: str = ""
    room_id: int | None = None
    source: str = ""
    locations_used: str = ""

    model_config = {"from_attributes": True}


class SigilRead(BaseModel):
    id: int
    name: str
    area: str = ""
    room: str = ""
    room_id: int | None = None
    source: str = ""
    door_unlocks: str = ""

    model_config = {"from_attributes": True}


class GrimoireRead(BaseModel):
    id: int
    name: str
    spell_name: str = ""
    area: str = ""
    room: str = ""
    room_id: int | None = None
    source: str = ""
    drop_rate: str = ""
    repeatable: bool = False

    model_config = {"from_attributes": True}


class GrimoireAggregated(BaseModel):
    id: int
    name: str
    spell_name: str = ""
    areas: str = ""
    sources: str = ""
    drop_rates: str = ""
    repeatable: bool = False


class BreakArtRead(BaseModel):
    id: int
    name: str
    weapon_type: str
    hp_cost: int
    attack_multiplier: str
    damage_type: str
    affinity: str
    special_effect: str | None = None
    kills_required: int

    model_config = {"from_attributes": True}


class BattleAbilityRead(BaseModel):
    id: int
    name: str
    ability_type: str
    risk_cost: int
    effect: str
    power: str

    model_config = {"from_attributes": True}


class CharacterRead(BaseModel):
    id: int
    name: str
    role: str
    description: str = ""

    model_config = {"from_attributes": True}


class TitleRead(BaseModel):
    id: int
    number: int
    name: str
    requirement: str = ""

    model_config = {"from_attributes": True}


class RankingRead(BaseModel):
    id: int
    level: int
    name: str
    requirement: str = ""

    model_config = {"from_attributes": True}


class WorkshopRead(BaseModel):
    id: int
    name: str
    area: str = ""
    room_id: int | None = None
    available_materials: str = ""
    description: str = ""

    model_config = {"from_attributes": True}


class CraftingRecipeRead(BaseModel):
    id: int
    category: str
    sub_category: str
    input_1: str
    input_2: str
    result: str
    tier_change: int
    has_swap: bool

    model_config = {"from_attributes": True}


class MaterialRecipeRead(BaseModel):
    id: int
    category: str
    sub_category: str
    input_1: str
    input_2: str
    material_1: str
    material_2: str
    result_material: str
    tier_change: int

    model_config = {"from_attributes": True}


# ── Enemy schemas ──────────────────────────────────────────────────────


class EnemyBodyPartRead(BaseModel):
    id: int
    enemy_id: int
    name: str
    physical: int = 0
    air: int = 0
    fire: int = 0
    earth: int = 0
    water: int = 0
    light: int = 0
    dark: int = 0
    blunt: int = 0
    edged: int = 0
    piercing: int = 0
    evade: int = 0
    chain_evade: int = 0

    model_config = {"from_attributes": True}


class EnemyRead(BaseModel):
    id: int
    name: str
    enemy_class: str
    hp: int
    mp: int
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    agi_stat: int = Field(serialization_alias="agi")
    encyclopaedia_number: int | None = None
    description: str = ""
    movement: int = 0
    is_boss: bool = False

    model_config = {"from_attributes": True, "populate_by_name": True}


class EncounterDropRead(BaseModel):
    id: int
    encounter_id: int
    body_part: str
    item: str
    material: str = ""
    drop_chance: str
    drop_value: int = 0
    grip: str = ""
    quantity: int = 1

    model_config = {"from_attributes": True}


class EnemyEncounterRead(BaseModel):
    id: int
    enemy_id: int
    room_id: int
    room_name: str = ""
    area_id: int = 0
    area_name: str = ""
    condition: str = ""
    attacks: str = ""
    drops: list[EncounterDropRead] = []

    model_config = {"from_attributes": True}


class EnemyDetailRead(BaseModel):
    id: int
    name: str
    enemy_class: str
    hp: int
    mp: int
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    agi_stat: int = Field(serialization_alias="agi")
    encyclopaedia_number: int | None = None
    description: str = ""
    movement: int = 0
    is_boss: bool = False
    body_parts: list[EnemyBodyPartRead] = []
    drops: list["EnemyDropRead"] = []
    encounters: list[EnemyEncounterRead] = []

    model_config = {"from_attributes": True, "populate_by_name": True}


class EnemyDropRead(BaseModel):
    id: int
    enemy_id: int
    body_part: str
    item: str
    material: str = ""
    drop_chance: str
    drop_value: int = 0
    grip: str = ""
    quantity: int = 1

    model_config = {"from_attributes": True}


# ── Inventory schemas ──────────────────────────────────────────────────


class InventoryItemCreate(BaseModel):
    item_type: str
    item_id: int
    material: str | None = None
    grip_id: int | None = None
    gem_1_id: int | None = None
    gem_2_id: int | None = None
    gem_3_id: int | None = None
    equip_slot: str | None = None
    storage: str = "bag"
    quantity: int = 1


class InventoryItemRead(BaseModel):
    id: int
    inventory_id: int
    item_type: str
    item_id: int
    material: str | None = None
    grip_id: int | None = None
    gem_1_id: int | None = None
    gem_2_id: int | None = None
    gem_3_id: int | None = None
    equip_slot: str | None = None
    storage: str = "bag"
    quantity: int = 1

    model_config = {"from_attributes": True}


class InventoryItemUpdate(BaseModel):
    item_type: str | None = None
    item_id: int | None = None
    material: str | None = None
    grip_id: int | None = None
    gem_1_id: int | None = None
    gem_2_id: int | None = None
    gem_3_id: int | None = None
    equip_slot: str | None = None
    storage: str | None = None
    quantity: int | None = None


class InventoryImportRequest(BaseModel):
    items: list[InventoryItemCreate]
    clear_existing: bool = False
    base_hp: int | None = None
    base_mp: int | None = None
    base_str: int | None = None
    base_int: int | None = None
    base_agi: int | None = None


class InventoryCreate(BaseModel):
    name: str


class InventoryUpdate(BaseModel):
    name: str


class InventoryListRead(BaseModel):
    id: int
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InventoryRead(BaseModel):
    id: int
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime
    base_hp: int | None = None
    base_mp: int | None = None
    base_str: int | None = None
    base_int: int | None = None
    base_agi: int | None = None
    items: list[InventoryItemRead] = []

    model_config = {"from_attributes": True}


# ── Game save import schemas ─────────────────────────────────────────


class GameSaveImportItem(BaseModel):
    """An item identified by field_name (stable across all DB instances)."""

    item_type: str  # blade / grip / armor / gem / consumable
    field_name: str  # e.g. "Power_Palm", "Khopesh"
    material: str | None = None
    grip_field_name: str | None = None
    gem_field_names: list[str] = []
    equip_slot: str | None = None
    storage: str = "bag"
    quantity: int = 1


class GameSaveImportRequest(BaseModel):
    """Create an inventory from a parsed game save file.

    Items are identified by field_name rather than database IDs,
    allowing external tools and clients to create inventories
    using stable game data identifiers.
    """

    name: str
    items: list[GameSaveImportItem]
    base_hp: int | None = None
    base_mp: int | None = None
    base_str: int | None = None
    base_int: int | None = None
    base_agi: int | None = None


class GameSaveImportResponse(BaseModel):
    inventory: InventoryRead
    warnings: list[str] = []


# ── Chest schemas ────────────────────────────────────────────────────


class ChestItemRead(BaseModel):
    id: int
    chest_id: int
    item_type: str
    item_name: str
    material: str | None = None
    gem_slots: int | None = None
    quantity: int = 1

    model_config = {"from_attributes": True}


class ChestListRead(BaseModel):
    id: int
    area: str
    room: str
    room_id: int | None = None
    lock_type: str | None = None

    model_config = {"from_attributes": True}


class ChestRead(BaseModel):
    id: int
    area: str
    room: str
    room_id: int | None = None
    lock_type: str | None = None
    items: list[ChestItemRead] = []

    model_config = {"from_attributes": True}


# ── Drop location schemas ────────────────────────────────────────────


class ItemDropLocationRead(BaseModel):
    enemy_name: str
    enemy_id: int
    enemy_class: str
    area_name: str
    area_id: int
    room_name: str
    body_part: str
    item: str
    material: str = ""
    drop_chance: str
    drop_value: int = 0
    grip: str = ""
    quantity: int = 1
    condition: str = ""

    model_config = {"from_attributes": True}


# ── Loadout optimizer schemas ────────────────────────────────────────


class LoadoutRequest(BaseModel):
    inventory_id: int
    enemy_id: int
    mode: str = "full"  # full / offense / defense
    include_equipped: bool = True
    include_bag: bool = True
    include_container: bool = True
    include_2h: bool = True
    # Optional player stats — if not provided, reads from inventory's base stats.
    # Pass explicitly for public API use without a saved inventory.
    player_str: int | None = None
    player_int: int | None = None
    player_agi: int | None = None


class LoadoutWeapon(BaseModel):
    blade_name: str
    blade_type: str
    grip_name: str | None = None
    material: str
    damage_type: str
    hands: str


class LoadoutArmor(BaseModel):
    slot: str
    item_name: str
    armor_type: str
    material: str


class LoadoutBodyPartScore(BaseModel):
    name: str
    estimated_damage: float = 0.0
    hit_chance: int = 100
    expected_damage: float = 0.0
    is_recommended: bool = False


class LoadoutStats(BaseModel):
    estimated_damage: float = 0.0
    hit_chance: int = 100
    expected_damage: float = 0.0
    target_body_part: str = ""
    target_reason: str = ""


class LoadoutCombinedStats(BaseModel):
    str_stat: int = Field(0, serialization_alias="str")
    int_stat: int = Field(0, serialization_alias="int")
    agi_stat: int = Field(0, serialization_alias="agi")
    range_stat: int = Field(0, serialization_alias="range")
    risk: int = 0
    damage_type: str = ""
    blunt: int = 0
    edged: int = 0
    piercing: int = 0
    human: int = 0
    beast: int = 0
    undead: int = 0
    phantom: int = 0
    dragon: int = 0
    evil: int = 0
    physical: int = 0
    fire: int = 0
    water: int = 0
    wind: int = 0
    earth: int = 0
    light: int = 0
    dark: int = 0

    model_config = {"from_attributes": True, "populate_by_name": True}


class LoadoutResult(BaseModel):
    rank: int
    score: float
    offense_score: float | None = None
    defense_score: float | None = None
    weapon: LoadoutWeapon | None = None
    armor: list[LoadoutArmor] | None = None
    stats: LoadoutStats = LoadoutStats()
    combined_stats: LoadoutCombinedStats | None = None
    body_parts: list[LoadoutBodyPartScore] = []


class LoadoutEnemyInfo(BaseModel):
    id: int
    name: str
    enemy_class: str
    hp: int
    mp: int


class LoadoutResponse(BaseModel):
    enemy: LoadoutEnemyInfo
    loadouts: list[LoadoutResult] = []
