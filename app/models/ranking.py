from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Ranking(Base):
    __tablename__ = "rankings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(100))
    requirement: Mapped[str] = mapped_column(String(200), default="")
