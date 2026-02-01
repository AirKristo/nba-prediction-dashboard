"""
Game Model

Show an NBA game either historical or scheduled
Will link to teams by a foreign key

"""

from datetime import date, datetime

from sqlalchemy import String, Integer, Boolean, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.team import Team


class Game(Base):
    __tablename__ = 'games'

    # Primary key will be game id
    game_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    # When the game is/was played
    game_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # Season year 2022 is the 2022-2023 season
    season: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Home team foreign key
    home_team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    # Away team foreign key
    away_team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    # Scores (will be NULL until game is complete)
    home_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    away_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Game status tracking
    game_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default='scheduled',
    )

    # Playoff flag
    is_playoffs: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # Timestamps for tracking data
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships to Team model
    # Can do game.home_team.team_name instead of a query

    home_team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[home_team_id],
    )

    away_team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[away_team_id],
    )

    def __repr__(self) -> str:
        return f"<Game {self.game_id}: {self.game_date}>"

    @property
    def is_complete(self) -> bool:
        # Check if game was played
        return self.game_status == "final"

    @property
    def home_win(self) -> bool | None:
        # Return true if home won , false for away, none if not complete
        if not self.is_complete:
            return None
        return self.home_score > self.away_score

    @property
    def point_differential(self) -> int | None:
        # home score minus away score, none is not complete
        if not self.is_complete:
            return None
        return self.home_score - self.away_score


