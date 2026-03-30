from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Ashley's base character stats (from save file import, nullable for blank inventories)
    base_hp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    base_mp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    base_str: Mapped[int | None] = mapped_column(Integer, nullable=True)
    base_int: Mapped[int | None] = mapped_column(Integer, nullable=True)
    base_agi: Mapped[int | None] = mapped_column(Integer, nullable=True)

    items: Mapped[list["InventoryItem"]] = relationship(
        back_populates="inventory", cascade="all, delete-orphan", lazy="selectin"
    )


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inventories.id", ondelete="CASCADE")
    )
    item_type: Mapped[str] = mapped_column(String(50))
    item_id: Mapped[int] = mapped_column(Integer)
    material: Mapped[str | None] = mapped_column(String(50), nullable=True)
    grip_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gem_1_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gem_2_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gem_3_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    equip_slot: Mapped[str | None] = mapped_column(String(20), nullable=True)
    storage: Mapped[str] = mapped_column(String(20), server_default="bag")
    quantity: Mapped[int] = mapped_column(Integer, server_default="1")

    # DP/PP stats from save file import (nullable for manually created items)
    dp_current: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dp_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pp_current: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pp_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    inventory: Mapped["Inventory"] = relationship(back_populates="items")
