from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Spell(Base):
    __tablename__ = "spells"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50))
    mp_cost: Mapped[str] = mapped_column(String(50), default="0")
    targeting: Mapped[str] = mapped_column(String(100), default="")
    affinity: Mapped[str] = mapped_column(String(50), default="")
    effect: Mapped[str] = mapped_column(Text, default="")
    grimoire: Mapped[str] = mapped_column(String(100), default="")
