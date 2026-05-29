from bs4.element import Tag
from fbref.extract.extract_match.extract_summary import extract_summary
from fbref.extract.save_table_bytes import save_table_bytes


def process_team_summary(
    bucket: str,
    template: str,
    league: str,
    season: int,
    fixture_id: str,
    match_data: Tag,
    team_side: str,
) -> None:
    """
    Extract and save cards and substitutions for a single team from the match summary.

    This function parses the match summary section for the given team side
    (home or away), extracts player card events and substitution events, and
    saves them as CSV files in the specified S3 bucket.

    Args:
        bucket (str): Name of the destination S3 bucket.
        template (str): Top-level template directory under which data will be stored.
        league (str): League identifier (e.g., "Premier-League").
        season (int): The season year (end year of the season).
        fixture_id (str): Unique identifier of the fixture/match.
        match_data (Tag): BeautifulSoup `<div>` (match summary container)
            containing cards and substitution information.
        team_side (str): Which side of the fixture this data belongs to, either
            "home" or "away".

    Return:
        None

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        - Saves two CSV files per team:
            * ``cards.csv`` → player booking events.
            * ``subs.csv`` → player substitution events.
        - Files are stored under the fixture directory in S3, grouped by team side.
    """
    card_bytes, sub_bytes = extract_summary(match_data, team_side)
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/cards.csv",
        card_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="cards",
    )
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/subs.csv",
        sub_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="subs",
    )
