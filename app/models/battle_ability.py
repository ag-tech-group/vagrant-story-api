from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BattleAbility(Base):
    __tablename__ = "battle_abilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    ability_type: Mapped[str] = mapped_column(String(20))
    risk_cost: Mapped[int] = mapped_column(Integer)
    effect: Mapped[str] = mapped_column(String(200))
    power: Mapped[str] = mapped_column(String(100))
