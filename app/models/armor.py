from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Armor(Base):
    __tablename__ = "armor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, default=0)
    field_name: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    description_fr: Mapped[str] = mapped_column(String(500), default="")
    wep_file_id: Mapped[int] = mapped_column(Integer, default=0)
    armor_type: Mapped[str] = mapped_column(String(50))
    str_stat: Mapped[int] = mapped_column("str", Integer, default=0)
    int_stat: Mapped[int] = mapped_column("int", Integer, default=0)
    agi_stat: Mapped[int] = mapped_column("agi", Integer, default=0)
    gem_slots: Mapped[int] = mapped_column(Integer, default=0)
