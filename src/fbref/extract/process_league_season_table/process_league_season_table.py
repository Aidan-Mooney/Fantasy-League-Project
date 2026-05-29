from os import environ
from io import BytesIO
from typing import List
from fbref.extract.get_soup import get_soup
from fbref.extract.process_league_season_table.extract_match_row import (
    extract_match_row,
)
from fbref.extract.save_table_bytes import save_table_bytes


EXTRACT_BUCKET = environ["EXTRACT_BUCKET"]


def process_league_season_table(template: str, league: str, season: int) -> List[str]:
    url = f"https://fbref.com/en/comps/9/{season - 1}-{season}/schedule/{season - 1}-{season}-{league}-Scores-and-Fixtures"
    soup = get_soup(url)

    table = soup.find(lambda tag: tag.name == "table")
    rows = table.find("tbody").find_all("tr")

    match_bytes = BytesIO()
    fixture_ids = []

    for row in rows:
        new_row_string = extract_match_row(row, fixture_ids)
        match_bytes.write(new_row_string.encode("utf-8"))

    key_prefix = f"{template}/{league}/{season - 1}-{season}"
    save_table_bytes(EXTRACT_BUCKET, f"{key_prefix}/matches.csv", match_bytes)
    return fixture_ids
