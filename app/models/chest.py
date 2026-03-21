from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Chest(Base):
    __tablename__ = "chests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    area: Mapped[str] = mapped_column(String(100))
    room: Mapped[str] = mapped_column(String(200))
    room_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("rooms.id"), nullable=True)
    lock_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    items: Mapped[list[ChestItem]] = relationship(
        back_populates="chest", cascade="all, delete-orphan", lazy="selectin"
    )
    room_rel: Mapped[Room | None] = relationship("Room", lazy="selectin")


class ChestItem(Base):
    __tablename__ = "chest_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chest_id: Mapped[int] = mapped_column(Integer, ForeignKey("chests.id", ondelete="CASCADE"))
    item_type: Mapped[str] = mapped_column(String(50))
    item_name: Mapped[str] = mapped_column(String(200))
    material: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gem_slots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, server_default="1")

    chest: Mapped[Chest] = relationship(back_populates="items")
