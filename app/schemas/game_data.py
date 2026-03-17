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

    model_config = {"from_attributes": True, "populate_by_name": True}


class GemRead(BaseModel):
    id: int
    game_id: int
    field_name: str
    name: str
    description_fr: str
    magnitude: str
    affinity_type: str

    model_config = {"from_attributes": True}


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
    effects: list | dict | None = None

    model_config = {"from_attributes": True}
