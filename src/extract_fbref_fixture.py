from pathlib import Path
from get_tables import get_tables
from shared_utils.get_soup import get_soup
from src.save_team_tables import save_team_tables


def extract_fbref_fixture(base_path, fixture_id):
    home_path = f"{base_path}/{fixture_id}/home"
    away_path = f"{base_path}/{fixture_id}/away"
    Path(home_path).mkdir(parents=True, exist_ok=True)
    Path(away_path).mkdir(parents=True, exist_ok=True)
    url = f"https://fbref.com/en/matches/{fixture_id}"
    soup = get_soup(url)
    soup_tables = get_tables(soup)
    save_team_tables(home_path, soup_tables[3:10], soup_tables[0], soup_tables[18])
    save_team_tables(away_path, soup_tables[10:17], soup_tables[1], soup_tables[19])
