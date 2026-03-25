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
