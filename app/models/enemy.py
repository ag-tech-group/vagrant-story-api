from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Enemy(Base):
    __tablename__ = "enemies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    enemy_class: Mapped[str] = mapped_column(String(50))
    hp: Mapped[int] = mapped_column(Integer, default=0)
    mp: Mapped[int] = mapped_column(Integer, default=0)
    str_stat: Mapped[int] = mapped_column("str", Integer, default=0)
    int_stat: Mapped[int] = mapped_column("int", Integer, default=0)
    agi_stat: Mapped[int] = mapped_column("agi", Integer, default=0)
    encyclopaedia_number: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    description: Mapped[str] = mapped_column(String(500), default="")
    movement: Mapped[int] = mapped_column(Integer, default=0)
    is_boss: Mapped[bool] = mapped_column(Boolean, default=False)

    body_parts: Mapped[list[EnemyBodyPart]] = relationship(
        back_populates="enemy", cascade="all, delete-orphan", lazy="selectin"
    )
    drops: Mapped[list[EnemyDrop]] = relationship(
        back_populates="enemy", cascade="all, delete-orphan", lazy="noload"
    )


class EnemyBodyPart(Base):
    __tablename__ = "enemy_body_parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enemy_id: Mapped[int] = mapped_column(Integer, ForeignKey("enemies.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    physical: Mapped[int] = mapped_column(Integer, default=0)
    air: Mapped[int] = mapped_column(Integer, default=0)
    fire: Mapped[int] = mapped_column(Integer, default=0)
    earth: Mapped[int] = mapped_column(Integer, default=0)
    water: Mapped[int] = mapped_column(Integer, default=0)
    light: Mapped[int] = mapped_column(Integer, default=0)
    dark: Mapped[int] = mapped_column(Integer, default=0)
    blunt: Mapped[int] = mapped_column(Integer, default=0)
    edged: Mapped[int] = mapped_column(Integer, default=0)
    piercing: Mapped[int] = mapped_column(Integer, default=0)
    evade: Mapped[int] = mapped_column(Integer, default=0)
    chain_evade: Mapped[int] = mapped_column(Integer, default=0)

    enemy: Mapped[Enemy] = relationship(back_populates="body_parts")


class EnemyDrop(Base):
    __tablename__ = "enemy_drops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enemy_id: Mapped[int] = mapped_column(Integer, ForeignKey("enemies.id", ondelete="CASCADE"))
    body_part: Mapped[str] = mapped_column(String(50))
    item: Mapped[str] = mapped_column(String(100))
    material: Mapped[str] = mapped_column(String(50), default="")
    drop_chance: Mapped[str] = mapped_column(String(50))
    drop_value: Mapped[int] = mapped_column(Integer, default=0)
    grip: Mapped[str] = mapped_column(String(100), default="")
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    enemy: Mapped[Enemy] = relationship(back_populates="drops")
