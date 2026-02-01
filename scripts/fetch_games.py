"""
Fetch Games Script

Pulls historical game data from the NBA API and loads it into the database.
Uses the nba_api library to fetch game logs by season.
"""

import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nba_api.stats.endpoints import leaguegamefinder
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models import Team, Game
from app.config import get_settings

settings = get_settings()

# Map NBA API team abbreviations to our database
# Some teams have different abbreviations in the API
#TEAM_ABBREV_MAP = {
#}


def get_team_id_map(db: Session) -> dict[str, int]:
    """
    Create a mapping of team abbreviation to team_id.
    """
    teams = db.query(Team).all()
    return {team.team_abbreviation: team.team_id for team in teams}


def fetch_season_games(season: int, db: Session, team_id_map: dict[str, int]) -> int:
    """
    Get all games for a given season from NBA API.

    Returns: Number of games added
    """
    print(f"\nGetting {season}-{str(season + 1)[-2:]} season...")

    # NBA API uses format "2024-25" for season
    season_str = f"{season}-{str(season + 1)[-2:]}"

    # Add delay to avoid rate limiting
    time.sleep(settings.nba_api_delay)

    try:
        # All games for the season
        # LeagueGameFinder returns games from the perspective of each team
        # So each game appears twice (once for each team)
        game_finder = leaguegamefinder.LeagueGameFinder(
            season_nullable=season_str,
            league_id_nullable="00",  # NBA
            season_type_nullable="Regular Season",
            timeout=settings.nba_api_timeout,
        )

        games_df = game_finder.get_data_frames()[0]

        if games_df.empty:
            print(f"  No games found for {season_str}")
            return 0

        print(f"  Found {len(games_df)} game records (each game counted twice)")

        # Process games - we'll see each game twice, once per team
        games_added = 0
        games_skipped = 0

        # Get unique game IDs
        unique_game_ids = games_df["GAME_ID"].unique()
        print(f"  Processing {len(unique_game_ids)} unique games...")

        for game_id in unique_game_ids:
            # Check if game already exists
            existing = db.query(Game).filter(Game.game_id == game_id).first()
            if existing:
                games_skipped += 1
                continue

            # Get both rows for this game (home and away team perspectives)
            game_rows = games_df[games_df["GAME_ID"] == game_id]

            if len(game_rows) != 2:
                print(f"  Warning: Game {game_id} has {len(game_rows)} rows, skipping")
                continue

            # Determine home and away teams
            # MATCHUP field contains "NYK vs. LAL" for home team, "LAL @ NYK" for away
            home_row = game_rows[game_rows["MATCHUP"].str.contains(" vs. ")].iloc[0] if len(
                game_rows[game_rows["MATCHUP"].str.contains(" vs. ")]) > 0 else None
            away_row = game_rows[game_rows["MATCHUP"].str.contains(" @ ")].iloc[0] if len(
                game_rows[game_rows["MATCHUP"].str.contains(" @ ")]) > 0 else None

            if home_row is None or away_row is None:
                print(f"  Warning: Could not determine home/away for game {game_id}, skipping")
                continue

            # Get team abbreviations
            home_abbrev = home_row["TEAM_ABBREVIATION"]
            away_abbrev = away_row["TEAM_ABBREVIATION"]

            # Map to our team IDs
            # home_abbrev = TEAM_ABBREV_MAP.get(home_abbrev, home_abbrev)
            # away_abbrev = TEAM_ABBREV_MAP.get(away_abbrev, away_abbrev)

            if home_abbrev not in team_id_map:
                print(f"  Warning: Unknown team {home_abbrev}, skipping game {game_id}")
                continue
            if away_abbrev not in team_id_map:
                print(f"  Warning: Unknown team {away_abbrev}, skipping game {game_id}")
                continue

            # Parse game date
            game_date = datetime.strptime(home_row["GAME_DATE"], "%Y-%m-%d").date()

            # Create game record
            game = Game(
                game_id=game_id,
                game_date=game_date,
                season=season,
                home_team_id=team_id_map[home_abbrev],
                away_team_id=team_id_map[away_abbrev],
                home_score=int(home_row["PTS"]) if home_row["PTS"] else None,
                away_score=int(away_row["PTS"]) if away_row["PTS"] else None,
                game_status="final",
                is_playoffs=False,
            )

            db.add(game)
            games_added += 1

            # Commit in batches of 100
            if games_added % 100 == 0:
                db.commit()
                print(f"  Added {games_added} games...")

        # Final commit
        db.commit()
        print(f"  Done! Added {games_added} games, skipped {games_skipped} existing")

        return games_added

    except Exception as e:
        print(f"  Error getting season {season}: {e}")
        db.rollback()
        raise


def main():
    parser = argparse.ArgumentParser(description="Get NBA game data")
    parser.add_argument("--season", type=int, help="Single season to collect (e.g., 2024)")
    parser.add_argument("--all", action="store_true", help="Get all seasons (2019-2024)")

    args = parser.parse_args()

    if not args.season and not args.all:
        print("Please specify --season YEAR or --all")
        print("Example: python scripts/fetch_games.py --season 2024")
        print("Example: python scripts/fetch_games.py --all")
        return

    # Determine which seasons to fetch
    if args.all:
        seasons = [2019, 2020, 2021, 2022, 2023, 2024]
    else:
        seasons = [args.season]

    print(f"Will fetch {len(seasons)} season(s): {seasons}")

    # Connect to database
    db = SessionLocal()

    try:
        # Get team ID mapping
        team_id_map = get_team_id_map(db)
        print(f"Loaded {len(team_id_map)} teams from database")

        if len(team_id_map) == 0:
            print("Error: No teams in database. Run seed_teams.py first.")
            return

        # Fetch each season
        total_games = 0
        for season in seasons:
            games_added = fetch_season_games(season, db, team_id_map)
            total_games += games_added

            # Add delay between seasons to avoid rate limiting
            if season != seasons[-1]:
                print("  Waiting before next season...")
                time.sleep(2)

        print(f"\n{'=' * 50}")
        print(f"Complete! Total games added: {total_games}")

    finally:
        db.close()


if __name__ == "__main__":
    main()