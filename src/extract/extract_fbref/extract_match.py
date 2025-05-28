from os import environ
from boto3 import client


from get_soup import get_soup


s3_client = client("s3")


def extract_match(event, context):
    process_tracking_bucket = environ["PROC_TRACK_BUCKET"]
    fixture_id = event["fixture_id"]
    league = event["league"]
    season = event["season"]
    url = f"https://fbref.com/en/matches/{fixture_id}"
    soup = get_soup(url)
    raw_html_tables = soup.find_all(lambda tag: tag.name == "table")
    process_match_tables(raw_html_tables)
    process_match_summary(soup)
    client.put_object(
        Bucket=process_tracking_bucket,
        Key=f"{league}/{season - 1}-{season}/{fixture_id}.json",
        Body="",
    )
    return {}


def process_match_tables(raw_html_tables):
    extract_bucket = environ["EXTRACT_BUCKET"]
    for table in raw_html_tables:
        csv = html_table_to_csv_string(table)
    return


def html_table_to_csv_string(html_table):
    return


def process_match_summary(soup):
    extract_bucket = environ["EXTRACT_BUCKET"]
    return
