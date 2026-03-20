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
    grip_type: int
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    agi_stat: int = Field(serialization_alias="agi")
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
