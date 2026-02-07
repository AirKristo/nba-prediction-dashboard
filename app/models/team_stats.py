from sqlalchemy import (
    Column, Integer, Float, Boolean, String,
    ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.session import Base


class TeamStats(Base):
    __tablename__ = "team_stats"

    stat_id = Column(Integer, primary_key=True, autoincrement=True)

    # Which team, which game, which season
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    game_id = Column(String(20), ForeignKey("games.game_id"), nullable=False)
    season = Column(Integer, nullable=False)

    # Record going into this game
    wins = Column(Integer, nullable=False, default=0)
    losses = Column(Integer, nullable=False, default=0)
    win_pct = Column(Float, nullable=False, default=0.0)

    # Rolling scoring stats (last 10 games)
    pts_per_game_last10 = Column(Float, nullable=True)
    opp_pts_per_game_last10 = Column(Float, nullable=True)

    # Rolling win counts
    last_5_wins = Column(Integer, nullable=True)
    last_10_wins = Column(Integer, nullable=True)

    # Home/away splits (season-to-date)
    home_win_pct = Column(Float, nullable=True)
    away_win_pct = Column(Float, nullable=True)

    # Rest
    days_rest = Column(Integer, nullable=True)
    is_back_to_back = Column(Boolean, nullable=False, default=False)

    # Streaks
    win_streak = Column(Integer, nullable=False, default=0)
    loss_streak = Column(Integer, nullable=False, default=0)

    # Simple ratings (season-to-date averages)
    avg_margin = Column(Float, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    team = relationship("Team")
    game = relationship("Game")

    # One stats row per team per game
    __table_args__ = (
        UniqueConstraint("team_id", "game_id", name="uq_team_game_stats"),
    )

    def __repr__(self):
        return f"<TeamStats team_id={self.team_id} game_id={self.game_id} record={self.wins}-{self.losses}>"