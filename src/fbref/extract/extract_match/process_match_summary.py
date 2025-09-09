from bs4 import BeautifulSoup
from fbref.extract.extract_match.process_team_summary import process_team_summary


def process_match_summary(
    bucket: str,
    template: str,
    league: str,
    season: int,
    fixture_id: str,
    soup: BeautifulSoup,
):
    """
    Extract and process the match summary for both home and away teams.

    This function locates the match summary section of the fixture page,
    delegates the parsing of team-specific data to ``process_team_summary``,
    and uploads the results to S3.

    Args:
        bucket (str): Name of the destination S3 bucket.
        template (str): Top-level template directory under which data will be stored.
        league (str): League identifier (e.g., "Premier-League").
        season (int): The season year (end year of the season).
        fixture_id (str): Unique identifier of the fixture/match.
        soup (BeautifulSoup): Parsed HTML of the fixture page.

    Returns:
        None

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).
    """
    match_data = soup.find("div", {"id": "events_wrap"})
    process_team_summary(
        bucket, template, league, season, fixture_id, match_data, "home"
    )
    process_team_summary(
        bucket, template, league, season, fixture_id, match_data, "away"
    )
