from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    tier: Mapped[int] = mapped_column(Integer)
    str_modifier: Mapped[int] = mapped_column(Integer, default=0)
    int_modifier: Mapped[int] = mapped_column(Integer, default=0)
    agi_modifier: Mapped[int] = mapped_column(Integer, default=0)
    human: Mapped[int] = mapped_column(Integer, default=0)
    beast: Mapped[int] = mapped_column(Integer, default=0)
    undead: Mapped[int] = mapped_column(Integer, default=0)
    phantom: Mapped[int] = mapped_column(Integer, default=0)
    dragon: Mapped[int] = mapped_column(Integer, default=0)
    evil: Mapped[int] = mapped_column(Integer, default=0)
    fire: Mapped[int] = mapped_column(Integer, default=0)
    water: Mapped[int] = mapped_column(Integer, default=0)
    wind: Mapped[int] = mapped_column(Integer, default=0)
    earth: Mapped[int] = mapped_column(Integer, default=0)
    light: Mapped[int] = mapped_column(Integer, default=0)
    dark: Mapped[int] = mapped_column(Integer, default=0)
