from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.enemy import Enemy
    from app.models.room import Room


class EnemyEncounter(Base):
    __tablename__ = "enemy_encounters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enemy_id: Mapped[int] = mapped_column(Integer, ForeignKey("enemies.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("rooms.id"))
    condition: Mapped[str] = mapped_column(String(500), default="")
    attacks: Mapped[str] = mapped_column(String(500), default="")

    enemy: Mapped[Enemy] = relationship("Enemy", back_populates="encounters")
    room: Mapped[Room] = relationship("Room", lazy="selectin")
    drops: Mapped[list[EncounterDrop]] = relationship(
        "EncounterDrop", cascade="all, delete-orphan", lazy="selectin"
    )


class EncounterDrop(Base):
    __tablename__ = "encounter_drops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    encounter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("enemy_encounters.id", ondelete="CASCADE")
    )
    body_part: Mapped[str] = mapped_column(String(50))
    item: Mapped[str] = mapped_column(String(100))
    material: Mapped[str] = mapped_column(String(50), default="")
    drop_chance: Mapped[str] = mapped_column(String(50))
    drop_value: Mapped[int] = mapped_column(Integer, default=0)
    grip: Mapped[str] = mapped_column(String(100), default="")
    quantity: Mapped[int] = mapped_column(Integer, default=1)
