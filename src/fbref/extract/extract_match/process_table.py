from bs4.element import Tag
from fbref.extract.save_table_bytes import save_table_bytes
from fbref.extract.extract_match.html_table_to_csv_bytes import html_table_to_csv_bytes


def process_table(
    bucket: str,
    template: str,
    league: str,
    season: int,
    fixture_id: str,
    team_side: str,
    table_name: str,
    table: Tag,
    table_schema: dict,
) -> None:
    """
    Transform and save a single statistics table to S3, if it matches the schema.

    This function checks whether the given table is defined in the provided
    ``table_schema``. If so, it converts the HTML table into CSV bytes and uploads
    the result to the appropriate S3 path.

    Args:
        bucket (str): Name of the destination S3 bucket.
        template (str): Top-level template directory under which data will be stored.
        league (str): League identifier (e.g., "Premier-League").
        season (int): The season year (end year of the season).
        fixture_id (str): Unique identifier of the fixture/match.
        team_side (str): Which side of the fixture this data belongs to, either
            "home" or "away".
        table_name (str): Descriptive name of the table (e.g., "Passing").
        team_tables (List[Tag]): A BeautifulSoup `<table>` element containing team statistics.
        table_schema (dict): Mapping of table names to schema definitions,
            used to process team statistic tables.

    Returns:
        None

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        - If ``table_name`` is not found in ``table_schema``, the table is skipped.
        - Processed files are saved in CSV format under the path:
          ``{template}/{league}/{season-1}-{season}/{fixture_id}/{team_side}/{table_name}.csv``.
    """
    headings = table_schema.get(table_name, None)
    if headings is not None:
        table_bytes = html_table_to_csv_bytes(table, headings)
        save_table_bytes(
            bucket,
            f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/{table_name}.csv",
            table_bytes,
            template=template,
            league=league,
            season=season,
            fixture_id=fixture_id,
            team_side=team_side,
            table_name=table_name,
        )
