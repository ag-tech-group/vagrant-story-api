from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Sigil(Base):
    __tablename__ = "sigils"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    area: Mapped[str] = mapped_column(String(100), default="")
    room: Mapped[str] = mapped_column(String(100), default="")
    source: Mapped[str] = mapped_column(String(200), default="")
    door_unlocks: Mapped[str] = mapped_column(Text, default="")
