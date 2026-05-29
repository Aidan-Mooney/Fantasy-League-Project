from io import BytesIO
from typing import List
from bs4.element import Tag
from fbref.extract.save_table_bytes import save_table_bytes
from fbref.extract.extract_match.process_lineup_data import process_lineup_data
from fbref.extract.extract_match.process_team_tables import process_team_tables


def process_match_tables(
    bucket: str,
    template: str,
    league: str,
    season: int,
    fixture_id: str,
    raw_html_tables: List[Tag],
    table_schema: dict,
) -> None:
    """
    Process lineup and team statistic tables for both home and away teams.

    This function:
      1. Extracts and saves the home and away team lineups (including formations).
      2. Processes team-specific statistic tables using the provided schema.
      3. Saves a match-info CSV containing each team's formation.

    Args:
        bucket (str): Name of the destination S3 bucket.
        template (str): Top-level template directory under which data will be stored.
        league (str): League identifier (e.g., "Premier-League").
        season (int): The season year (end year of the season).
        fixture_id (str): Unique identifier of the fixture/match.
        raw_html_tables (List[Tag]): List of BeautifulSoup `<table>` elements
            extracted from the fixture page, in their original order.
        table_schema (dict): Mapping of table names to schema definitions,
            used to process team statistic tables.

    Returns:
        None

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        - The first two tables in ``raw_html_tables`` are expected to be the
          home and away lineup tables, respectively.
        - Subsequent slices of ``raw_html_tables`` are assumed to map to specific
          team statistic tables by index.
        - The function produces a ``match-info.csv`` file containing both teams’
          formations, saved under the fixture directory.
    """
    home_formation = process_lineup_data(
        bucket, template, league, season, fixture_id, "home", raw_html_tables[0]
    )
    home_tables = raw_html_tables[3:10] + [raw_html_tables[18]]
    process_team_tables(
        bucket,
        template,
        league,
        season,
        fixture_id,
        "home",
        home_tables,
        table_schema,
    )

    away_formation = process_lineup_data(
        bucket, template, league, season, fixture_id, "away", raw_html_tables[1]
    )
    away_tables = raw_html_tables[10:17] + [raw_html_tables[19]]
    process_team_tables(
        bucket,
        template,
        league,
        season,
        fixture_id,
        "away",
        away_tables,
        table_schema,
    )

    team_info_bytes = BytesIO()
    team_info_bytes.write("side,formation\n".encode("utf-8"))
    team_info_bytes.write(f"home,{home_formation}\n".encode("utf-8"))
    team_info_bytes.write(f"away,{away_formation}\n".encode("utf-8"))
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/match-info.csv",
        team_info_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        table_name="match-info",
    )
