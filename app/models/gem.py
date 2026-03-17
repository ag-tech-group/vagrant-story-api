from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Gem(Base):
    __tablename__ = "gems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, default=0)
    field_name: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    description_fr: Mapped[str] = mapped_column(String(500), default="")
    magnitude: Mapped[str] = mapped_column(String(50), default="")
    affinity_type: Mapped[str] = mapped_column(String(50), default="")
