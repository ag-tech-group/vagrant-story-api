from datetime import datetime

from pydantic import BaseModel, Field


class WeaponRead(BaseModel):
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
    source: str = ""
    locations_used: str = ""

    model_config = {"from_attributes": True}


class SigilRead(BaseModel):
    id: int
    name: str
    area: str = ""
    room: str = ""
    source: str = ""
    door_unlocks: str = ""

    model_config = {"from_attributes": True}


class GrimoireRead(BaseModel):
    id: int
    name: str
    spell_name: str = ""
    area: str = ""
    room: str = ""
    source: str = ""
    drop_rate: str = ""
    repeatable: bool = False

    model_config = {"from_attributes": True}


class WorkshopRead(BaseModel):
    id: int
    name: str
    area: str = ""
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


# ── Inventory schemas ──────────────────────────────────────────────────


class InventoryItemCreate(BaseModel):
    item_type: str
    item_id: int
    material: str | None = None
    grip_id: int | None = None
    gem_1_id: int | None = None
    gem_2_id: int | None = None
    gem_3_id: int | None = None
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
    quantity: int | None = None


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
    items: list[InventoryItemRead] = []

    model_config = {"from_attributes": True}
