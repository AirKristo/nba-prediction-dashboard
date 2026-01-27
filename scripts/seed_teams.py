# Populate the teams table with all 30 NBA teams
# Run this once after setting up the database
# python scripts/seed_teams.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.database.session import engine, SessionLocal
from app.models import Team

# All 30 NBA teams with their divisions and conferences
NBA_TEAMS = [
    # Eastern Conference - Atlantic Division
    {"team_abbreviation": "BOS", "team_name": "Boston Celtics", "conference": "East", "division": "Atlantic"},
    {"team_abbreviation": "BKN", "team_name": "Brooklyn Nets", "conference": "East", "division": "Atlantic"},
    {"team_abbreviation": "NYK", "team_name": "New York Knicks", "conference": "East", "division": "Atlantic"},
    {"team_abbreviation": "PHI", "team_name": "Philadelphia 76ers", "conference": "East", "division": "Atlantic"},
    {"team_abbreviation": "TOR", "team_name": "Toronto Raptors", "conference": "East", "division": "Atlantic"},

    # Eastern Conference - Central Division
    {"team_abbreviation": "CHI", "team_name": "Chicago Bulls", "conference": "East", "division": "Central"},
    {"team_abbreviation": "CLE", "team_name": "Cleveland Cavaliers", "conference": "East", "division": "Central"},
    {"team_abbreviation": "DET", "team_name": "Detroit Pistons", "conference": "East", "division": "Central"},
    {"team_abbreviation": "IND", "team_name": "Indiana Pacers", "conference": "East", "division": "Central"},
    {"team_abbreviation": "MIL", "team_name": "Milwaukee Bucks", "conference": "East", "division": "Central"},

    # Eastern Conference - Southeast Division
    {"team_abbreviation": "ATL", "team_name": "Atlanta Hawks", "conference": "East", "division": "Southeast"},
    {"team_abbreviation": "CHA", "team_name": "Charlotte Hornets", "conference": "East", "division": "Southeast"},
    {"team_abbreviation": "MIA", "team_name": "Miami Heat", "conference": "East", "division": "Southeast"},
    {"team_abbreviation": "ORL", "team_name": "Orlando Magic", "conference": "East", "division": "Southeast"},
    {"team_abbreviation": "WAS", "team_name": "Washington Wizards", "conference": "East", "division": "Southeast"},

    # Western Conference - Northwest Division
    {"team_abbreviation": "DEN", "team_name": "Denver Nuggets", "conference": "West", "division": "Northwest"},
    {"team_abbreviation": "MIN", "team_name": "Minnesota Timberwolves", "conference": "West", "division": "Northwest"},
    {"team_abbreviation": "OKC", "team_name": "Oklahoma City Thunder", "conference": "West", "division": "Northwest"},
    {"team_abbreviation": "POR", "team_name": "Portland Trail Blazers", "conference": "West", "division": "Northwest"},
    {"team_abbreviation": "UTA", "team_name": "Utah Jazz", "conference": "West", "division": "Northwest"},

    # Western Conference - Pacific Division
    {"team_abbreviation": "GSW", "team_name": "Golden State Warriors", "conference": "West", "division": "Pacific"},
    {"team_abbreviation": "LAC", "team_name": "Los Angeles Clippers", "conference": "West", "division": "Pacific"},
    {"team_abbreviation": "LAL", "team_name": "Los Angeles Lakers", "conference": "West", "division": "Pacific"},
    {"team_abbreviation": "PHX", "team_name": "Phoenix Suns", "conference": "West", "division": "Pacific"},
    {"team_abbreviation": "SAC", "team_name": "Sacramento Kings", "conference": "West", "division": "Pacific"},

    # Western Conference - Southwest Division
    {"team_abbreviation": "DAL", "team_name": "Dallas Mavericks", "conference": "West", "division": "Southwest"},
    {"team_abbreviation": "HOU", "team_name": "Houston Rockets", "conference": "West", "division": "Southwest"},
    {"team_abbreviation": "MEM", "team_name": "Memphis Grizzlies", "conference": "West", "division": "Southwest"},
    {"team_abbreviation": "NOP", "team_name": "New Orleans Pelicans", "conference": "West", "division": "Southwest"},
    {"team_abbreviation": "SAS", "team_name": "San Antonio Spurs", "conference": "West", "division": "Southwest"},
]

def seed_teams() -> None:
    # Insert all 30 NBA teams and skips teams already in

    db = SessionLocal()

    try:
        teams_added = 0
        teams_skipped = 0

        for team_data in NBA_TEAMS:
            existing = db.query(Team).filter(
                Team.team_abbreviation == team_data["team_abbreviation"]
            ).first()

            if existing:
                print(f"Skipping {team_data['team_abbreviation']} - already exists")
                teams_skipped += 1
                continue

            team = Team (**team_data)
            db.add(team)
            print(f"Added {team_data['team_abbreviation']}")
            teams_added += 1

        db.commit()

        print(f"\nDone! Added {teams_added} teams, skipped {teams_skipped}.")


    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding NBA teams...")
    seed_teams()