from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.database import Base


class Consumable(Base):
    __tablename__ = "consumables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, default=0)
    field_name: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    description_fr: Mapped[str] = mapped_column(String(500), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    effects: Mapped[dict | None] = mapped_column(JSON, nullable=True)
