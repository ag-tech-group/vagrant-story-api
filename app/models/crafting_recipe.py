from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CraftingRecipe(Base):
    __tablename__ = "crafting_recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    sub_category: Mapped[str] = mapped_column(String(100), index=True)
    input_1: Mapped[str] = mapped_column(String(100), index=True)
    input_2: Mapped[str] = mapped_column(String(100), index=True)
    result: Mapped[str] = mapped_column(String(100), index=True)
    tier_change: Mapped[int] = mapped_column(Integer, default=0)
    has_swap: Mapped[bool] = mapped_column(Boolean, default=False)


class MaterialRecipe(Base):
    __tablename__ = "material_recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    sub_category: Mapped[str] = mapped_column(String(100))
    input_1: Mapped[str] = mapped_column(String(100))
    input_2: Mapped[str] = mapped_column(String(100))
    material_1: Mapped[str] = mapped_column(String(50))
    material_2: Mapped[str] = mapped_column(String(50))
    result_material: Mapped[str] = mapped_column(String(50))
    tier_change: Mapped[int] = mapped_column(Integer, default=0)
