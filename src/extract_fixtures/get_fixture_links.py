import re
from os import environ
from boto3 import client
from typing import List, Tuple
from logging import getLogger, basicConfig, INFO
from requests.exceptions import HTTPError
from botocore.exceptions import ClientError


from get_soup import get_soup


basicConfig(level=INFO)
logger = getLogger(__name__)
s3_client = client("s3")


def lambda_handler(event: dict, context: dict) -> List[str]:
    try:
        validate_event(event)
    except TypeError as err:
        logger.critical("Event validation failed: %s | Event: %s", err, event)
        return {"success": False, "links": [], "error": str(err)}

    league = event["league"]
    season = event["season"]
    try:
        all_links = get_fixture_links(league, season)
    except HTTPError as err:
        logger.critical(
            "Failed to get fixture links for league=%s, season=%d: %s",
            league,
            season,
            err,
        )
        return {"success": False, "links": [], "error": str(err)}
    try:
        extracted_matches = get_processed_codes(league, season)
    except ClientError as err:
        logger.critical(
            "Failed to fetch processed match codes for league=%s, season=%s: %s",
            league,
            season,
            err,
        )
        return {"success": False, "links": [], "error": str(err)}
    links = list(set(all_links) - set(extracted_matches))
    logger.info(
        "Identified %d new fixture links for league=%s, season=%s",
        len(links),
        league,
        season,
    )
    return {"success": True, "links": links, "count": len(links)}


def validate_event(event: dict) -> None:
    expected_keys = {"league", "season"}
    if not isinstance(event, dict):
        raise TypeError("event must be a dictionary")
    actual_keys = set(event.keys())
    if actual_keys != expected_keys:
        raise TypeError("event must contain only the keys {'league', 'season'}")
    elif not isinstance(event["league"], str):
        raise TypeError("league value must be a string")
    elif not isinstance(event["season"], int):
        raise TypeError("season value must be an int")


def get_fixture_links(league: str, season: int) -> List[str]:
    url, regex_string = get_url_and_regex(league, season)
    soup = get_soup(url)
    link_condition = re.compile(regex_string)
    urls = set()
    for link in soup.find_all("a"):
        data = link.get("href")
        if data is None:
            continue
        elif link_condition.search(data):
            urls.add(data[12:20])
    return list(urls)


def get_url_and_regex(league: str, season: int) -> Tuple[str, str]:
    url = f"https://fbref.com/en/comps/9/{season - 1}-{season}/schedule/{season - 1}-{season}-{league}-Scores-and-Fixtures"
    regex_string = r"/en/matches/[a-z\d]{8}/[\w\d-]+-" + league
    return url, regex_string


def get_processed_codes(league: str, season: int) -> List[str]:
    bucket = environ["EXTRACT_BUCKET"]
    prefix = f"{league}/{season - 1}-{season}/"
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    keys = [obj["Key"] for obj in response.get("Contents", [])]
    codes = [key.removeprefix(prefix).removesuffix(".json") for key in keys]
    return codes
