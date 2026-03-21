from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BreakArt(Base):
    __tablename__ = "break_arts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    weapon_type: Mapped[str] = mapped_column(String(50))
    hp_cost: Mapped[int] = mapped_column(Integer)
    attack_multiplier: Mapped[str] = mapped_column(String(20))
    damage_type: Mapped[str] = mapped_column(String(20))
    affinity: Mapped[str] = mapped_column(String(50))
    special_effect: Mapped[str | None] = mapped_column(String(100), nullable=True)
    kills_required: Mapped[int] = mapped_column(Integer)
