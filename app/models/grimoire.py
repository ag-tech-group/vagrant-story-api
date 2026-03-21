from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Grimoire(Base):
    __tablename__ = "grimoires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    spell_name: Mapped[str] = mapped_column(String(100), default="")
    area: Mapped[str] = mapped_column(String(100), default="")
    room: Mapped[str] = mapped_column(String(200), default="")
    room_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("rooms.id"), nullable=True)
    source: Mapped[str] = mapped_column(String(200), default="")
    drop_rate: Mapped[str] = mapped_column(String(50), default="")
    repeatable: Mapped[bool] = mapped_column(Boolean, default=False)

    room_rel: Mapped[Room | None] = relationship("Room", lazy="selectin")
