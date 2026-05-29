from typing import List
from bs4.element import Tag
from fbref.extract.extract_match.process_table import process_table


table_name_dict = {
    0: "Summary",
    1: "Passing",
    2: "Pass Types",
    3: "Defensive Actions",
    4: "Possession",
    5: "Miscellaneous Stats",
    6: "Goalkeeper",
    7: "Shots",
}


def process_team_tables(
    bucket: str,
    template: str,
    league: str,
    season: int,
    fixture_id: str,
    team_side: str,
    team_tables: List[Tag],
    table_schema: dict,
) -> None:
    """
    Process and save all statistic tables for a single team.

    This function iterates over the provided HTML tables, assigns each one
    a descriptive name using ``table_name_dict``, and passes it to
    ``process_table`` for transformation and upload to S3.

    Args:
        bucket (str): Name of the destination S3 bucket.
        template (str): Top-level template directory under which data will be stored.
        league (str): League identifier (e.g., "Premier-League").
        season (int): The season year (end year of the season).
        fixture_id (str): Unique identifier of the fixture/match.
        team_side (str): Which side of the fixture this data belongs to, either
            "home" or "away".
        team_tables (List[Tag]): List of BeautifulSoup `<table>` elements
            extracted from the fixture page, in their original order.
        table_schema (dict): Mapping of table names to schema definitions,
            used to process team statistic tables.

    Returns:
        None

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        - The order of ``team_tables`` must match the keys in ``table_name_dict``.
        - Each table is saved under its descriptive name (e.g., "Passing",
          "Defensive Actions").
    """
    for index, table in enumerate(team_tables):
        table_name = table_name_dict[index]
        process_table(
            bucket,
            template,
            league,
            season,
            fixture_id,
            team_side,
            table_name,
            table,
            table_schema,
        )
