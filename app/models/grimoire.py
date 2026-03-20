from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Grimoire(Base):
    __tablename__ = "grimoires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    spell_name: Mapped[str] = mapped_column(String(100), default="")
    area: Mapped[str] = mapped_column(String(100), default="")
    room: Mapped[str] = mapped_column(String(200), default="")
    source: Mapped[str] = mapped_column(String(200), default="")
    drop_rate: Mapped[str] = mapped_column(String(50), default="")
    repeatable: Mapped[bool] = mapped_column(Boolean, default=False)
