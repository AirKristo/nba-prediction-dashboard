"""

Team model to represent an NBA team. Functional table that other tables
will reference with foreign keys

"""

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

class Team(Base):
    __tablename__ = "teams"

    team_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_abbreviation: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
        index=True,
    )

    team_name: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    conference: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    division: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Team {self.team_abbreviation}: {self.team_name}>"