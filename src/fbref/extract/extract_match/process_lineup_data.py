import re
from bs4.element import Tag
from fbref.extract.extract_match.configure_players_bytes import configure_players_bytes
from fbref.extract.save_table_bytes import save_table_bytes


def process_lineup_data(
    bucket: str,
    template: str,
    league: str,
    season: int,
    fixture_id: str,
    team_side: str,
    table: Tag,
) -> str:
    """
    Extract and save lineup data (starters and bench) from an HTML table.

    This function parses a lineup table from a football fixture, identifies the
    team formation, splits the table into starters and bench players, converts
    both into CSV bytes, and uploads them to the specified S3 bucket.

    Args:
        bucket (str): Name of the destination S3 bucket.
        template (str): Top-level template directory under which data will be stored.
        league (str): League identifier (e.g., "Premier-League").
        season (int): The season year (end year of the season).
        fixture_id (str): Unique identifier of the fixture/match.
        team_side (str): Which side of the fixture this data belongs to, either
            "home" or "away".
        table (Tag): BeautifulSoup `<table>` element containing the
            lineup HTML.

    Returns:
        str: The team formation (e.g., "4-3-3") extracted from the table header.

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        The function assumes the first header row contains the team name and
        formation in the form "Team Name (4-4-2)". It also assumes the table has
        a header row separating starters from bench players.
    """
    rows = table.find_all("tr")

    first_header = rows[0].find("th").get_text(strip=True)
    name_formation_condition = re.compile(r"^(.*?)\s*\(([\d\-]+)\)")
    name_formation_match = name_formation_condition.match(first_header)
    formation = name_formation_match.group(2).strip()

    second_header_index = None
    for i, row in enumerate(rows[1:], 1):
        th = row.find("th")
        if th and th.has_attr("colspan"):
            second_header_index = i
            break

    starters_bytes = configure_players_bytes(rows[1:second_header_index])
    bench_bytes = configure_players_bytes(rows[second_header_index + 1 :])
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/starters.csv",
        starters_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="starters",
    )
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/bench.csv",
        bench_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="bench",
    )
    return formation
