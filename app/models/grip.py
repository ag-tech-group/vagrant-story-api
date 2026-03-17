from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Grip(Base):
    __tablename__ = "grips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, default=0)
    field_name: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    description_fr: Mapped[str] = mapped_column(String(500), default="")
    wep_file_id: Mapped[int] = mapped_column(Integer, default=0)
    grip_type: Mapped[int] = mapped_column(Integer, default=0)
    str_stat: Mapped[int] = mapped_column("str", Integer, default=0)
    int_stat: Mapped[int] = mapped_column("int", Integer, default=0)
    agi_stat: Mapped[int] = mapped_column("agi", Integer, default=0)
    dp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pp: Mapped[int | None] = mapped_column(Integer, nullable=True)
