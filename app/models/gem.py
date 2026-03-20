from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Gem(Base):
    __tablename__ = "gems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, default=0)
    field_name: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    description_fr: Mapped[str] = mapped_column(String(500), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    magnitude: Mapped[str] = mapped_column(String(50), default="")
    affinity_type: Mapped[str] = mapped_column(String(50), default="")
    gem_type: Mapped[str] = mapped_column(String(50), default="")
    str_stat: Mapped[int] = mapped_column("str", Integer, default=0)
    int_stat: Mapped[int] = mapped_column("int", Integer, default=0)
    agi_stat: Mapped[int] = mapped_column("agi", Integer, default=0)
    # Class affinities
    human: Mapped[int] = mapped_column(Integer, default=0)
    beast: Mapped[int] = mapped_column(Integer, default=0)
    undead: Mapped[int] = mapped_column(Integer, default=0)
    phantom: Mapped[int] = mapped_column(Integer, default=0)
    dragon: Mapped[int] = mapped_column(Integer, default=0)
    evil: Mapped[int] = mapped_column(Integer, default=0)
    # Elemental affinities
    physical: Mapped[int] = mapped_column(Integer, default=0)
    fire: Mapped[int] = mapped_column(Integer, default=0)
    water: Mapped[int] = mapped_column(Integer, default=0)
    wind: Mapped[int] = mapped_column(Integer, default=0)
    earth: Mapped[int] = mapped_column(Integer, default=0)
    light: Mapped[int] = mapped_column(Integer, default=0)
    dark: Mapped[int] = mapped_column(Integer, default=0)
