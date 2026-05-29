from os import environ
from get_soup import get_soup
from fbref.extract.extract_match.get_schema import get_schema
from fbref.extract.extract_match.process_match_tables import process_match_tables
from fbref.extract.extract_match.process_match_summary import process_match_summary
from fbref.extract.save_table_bytes import save_table_bytes


EXTRACT_BUCKET = environ["EXTRACT_BUCKET"]
PROCESS_TRACKING_BUCKET = environ["PROC_TRACK_BUCKET"]


def extract_match(template: str, league: str, season: int, fixture_id: str) -> None:
    key_prefix = f"{template}/{league}/{season - 1}-{season}/{fixture_id}"
    url = f"https://fbref.com/en/matches/{fixture_id}"

    soup = get_soup(url)

    raw_html_tables = soup.find_all(lambda tag: tag.name == "table")

    table_schema = get_schema(template)
    process_match_tables(
        EXTRACT_BUCKET,
        template,
        league,
        season,
        fixture_id,
        raw_html_tables,
        table_schema,
    )
    process_match_summary(EXTRACT_BUCKET, template, league, season, fixture_id, soup)
    save_table_bytes(
        PROCESS_TRACKING_BUCKET,
        f"{key_prefix}.json",
        "",
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        table_name="extract_tracking_code",
    )
