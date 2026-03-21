from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Sigil(Base):
    __tablename__ = "sigils"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    area: Mapped[str] = mapped_column(String(100), default="")
    room: Mapped[str] = mapped_column(String(100), default="")
    room_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("rooms.id"), nullable=True)
    source: Mapped[str] = mapped_column(String(200), default="")
    door_unlocks: Mapped[str] = mapped_column(Text, default="")

    room_rel: Mapped[Room | None] = relationship("Room", lazy="selectin")
