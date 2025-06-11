import re
import json
from os import environ
from boto3 import client
from logging import getLogger, basicConfig, INFO
from requests.exceptions import HTTPError
from botocore.exceptions import ClientError


from get_soup import get_soup
from list_to_csv import list_to_csv


basicConfig(level=INFO)
logger = getLogger(__name__)
s3_client = client("s3")


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


def extract_match(event, context):
    try:
        validate_event(event)
    except TypeError as err:
        logger.critical("Event validation failed: %s | Event: %s", err, event)
        return {"success": False, "links": [], "error": str(err)}

    template = event["template"]
    league = event["league"]
    season = event["season"]
    fixture_id = event["fixture_id"]
    key_prefix = f"{template}/{league}/{season - 1}-{season}/{fixture_id}"

    process_tracking_bucket = environ["PROC_TRACK_BUCKET"]
    extract_bucket = environ["EXTRACT_BUCKET"]
    template_bucket = environ["TEMPLATE_BUCKET"]

    log_messages = []

    try:
        url = f"https://fbref.com/en/matches/{fixture_id}"
        soup = get_soup(url)
    except HTTPError as err:
        logger.critical(
            "Failed to retrieve soup for league=%s, season=%s, fixture_id=%s: %s",
            league,
            season,
            fixture_id,
            err,
        )
        return {"success": False, "error": str(err)}

    raw_html_tables = soup.find_all(lambda tag: tag.name == "table")

    try:
        response = s3_client.get_object(Bucket=template_bucket, Key=f"{template}.json")
        table_schema = json.load(response["Body"])
    except ClientError as err:
        logger.critical(
            "Failed to fetch match template=%s for league=%s, season=%s: %s",
            template,
            league,
            season,
            err,
        )
        return {"success": False, "error": str(err)}

    try:
        process_match_tables(
            extract_bucket, key_prefix, raw_html_tables, table_schema, log_messages
        )
        process_match_summary(extract_bucket, key_prefix, soup, log_messages)
        s3_client.put_object(
            Bucket=process_tracking_bucket,
            Key=f"{key_prefix}.json",
            Body="",
        )
    except ClientError as err:
        logger.critical(
            "Failed to put match data for template=%s, league=%s, season=%s, fixture_id=%s: %s",
            template,
            league,
            season,
            fixture_id,
            err,
        )
        return {"success": False, "error": str(err)}
    message = "\n".join(log_messages)
    logger.info(
        "Processed fixture fixture_id=%s for template=%s, league=%s, season=%s\n%s",
        fixture_id,
        template,
        league,
        season,
        message,
    )
    return {"success": True}


def validate_event(event: dict) -> None:
    expected_keys = {"template", "league", "season", "fixture_id"}
    if not isinstance(event, dict):
        raise TypeError("event must be a dictionary")
    actual_keys = set(event.keys())
    if actual_keys != expected_keys:
        raise TypeError(
            "event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
        )
    elif not isinstance(event["template"], str):
        raise TypeError("template value must be a string")
    elif not isinstance(event["league"], str):
        raise TypeError("league value must be a string")
    elif not isinstance(event["season"], int):
        raise TypeError("season value must be an int")
    elif not isinstance(event["fixture_id"], str):
        raise TypeError("fixture_id value must be a string")


def process_match_tables(
    bucket, key_prefix, raw_html_tables, table_schema: dict, log_messages
):
    home_team_info = process_lineup_data(raw_html_tables[0])
    home_tables = raw_html_tables[3:10] + [raw_html_tables[18]]
    process_team_tables(
        bucket,
        key_prefix,
        "home",
        home_team_info,
        home_tables,
        table_schema,
        log_messages,
    )

    away_team_info = process_lineup_data(raw_html_tables[1])
    away_tables = raw_html_tables[10:17] + [raw_html_tables[19]]
    process_team_tables(
        bucket,
        key_prefix,
        "away",
        away_team_info,
        away_tables,
        table_schema,
        log_messages,
    )

    home_team = home_team_info[0]
    home_formation = home_team_info[1]
    away_team = away_team_info[0]
    away_formation = away_team_info[1]
    team_info_body = (
        "side,team,formation\n"
        + f"home,{home_team},{home_formation}\n"
        + f"away,{away_team},{away_formation}\n"
    )
    s3_client.put_object(
        Bucket=bucket, Key=f"{key_prefix}/match-info.csv", Body=team_info_body
    )
    log_messages.append("processed match info.")


def process_team_tables(
    bucket, key_prefix, team_side, team_info, team_tables, table_schema, log_messages
):
    _, _, starters, bench = team_info
    starters_csv = list_to_csv(("Shirt Number", "Player"), starters)
    bench_csv = list_to_csv(("Shirt Number", "Player"), bench)
    s3_client.put_object(
        Bucket=bucket, Key=f"{key_prefix}/{team_side}/starters.csv", Body=starters_csv
    )
    log_messages.append(f"processed {team_side} team starters.")
    s3_client.put_object(
        Bucket=bucket, Key=f"{key_prefix}/{team_side}/bench.csv", Body=bench_csv
    )
    log_messages.append(f"processed {team_side} team bench.")

    for index, table in enumerate(team_tables):
        table_name = table_name_dict[index]
        process_table(
            bucket,
            key_prefix,
            team_side,
            table_name,
            table,
            table_schema,
            log_messages,
        )


def process_lineup_data(table):
    rows = table.find_all("tr")

    first_header = rows[0].find("th").get_text(strip=True)
    name_formation_condition = re.compile(r"^(.*?)\s*\(([\d\-]+)\)")
    name_formation_match = name_formation_condition.match(first_header)
    team_name = name_formation_match.group(1).strip()
    formation = name_formation_match.group(2).strip()

    second_header_index = None
    for i, row in enumerate(rows[1:], 1):
        th = row.find("th")
        if th and th.has_attr("colspan"):
            second_header_index = i
            break

    starters = html_helper(rows[1:second_header_index])
    bench = html_helper(rows[second_header_index + 1 :])
    return team_name, formation, starters, bench


def process_table(
    bucket, key_prefix, team_side, table_name, table, table_schema, log_messages
):
    headings = table_schema.get(table_name, None)
    if headings is not None:
        csv = html_table_to_csv_string(table, headings)
        s3_client.put_object(
            Bucket=bucket,
            Key=f"{key_prefix}/{team_side}/{table_name}.csv",
            Body=csv,
        )
        log_messages.append(f"processed {team_side} team {table_name} table.")


def html_table_to_csv_string(table, cols=None):
    header_rows = table.find("thead").find_all("tr")

    headers = []
    ignore_rows = []
    if len(header_rows) == 2:
        top_row = header_rows[0]
        expanded_top = []
        for th in top_row.find_all("th"):
            colspan = int(th.get("colspan", 1))
            text = th.get_text(strip=True)
            expanded_top.extend([text] * colspan)
    for index, th in enumerate(header_rows[-1].find_all("th")):
        normal_col = th.get_text(strip=True)
        if len(header_rows) == 2:
            top_col = expanded_top[index]
            heading = f"{top_col} {normal_col}".strip() if top_col else normal_col
        else:
            heading = normal_col
        if cols is None:
            headers.append(heading)
        elif heading in cols:
            headers.append(heading)
        else:
            ignore_rows.append(index)

    csv_string = ",".join(headers) + "\n"

    for tr in table.find("tbody").find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row = [
            cell.get_text(strip=True)
            for index, cell in enumerate(cells)
            if index not in ignore_rows
        ]
        if row:
            csv_string += ",".join(row) + "\n"
    return csv_string


def html_helper(rows):
    players = []
    for row in rows:
        tds = row.find_all("td")
        if len(tds) == 2:
            shirt_number = tds[0].get_text(strip=True)
            for div in tds[1].find_all("div"):
                div.decompose()
            name = tds[1].get_text(strip=True)
            players.append((shirt_number, name))
    return players


def process_match_summary(bucket, key_prefix, soup, log_messages):
    match_data = soup.find("div", {"id": "events_wrap"})
    process_team_summary(bucket, key_prefix, match_data, "home", log_messages)
    process_team_summary(bucket, key_prefix, match_data, "away", log_messages)


def process_team_summary(bucket, key_prefix, match_data, team_side, log_messages):
    card_csv, sub_csv = extract_summary(match_data, team_side)
    s3_client.put_object(
        Bucket=bucket, Key=f"{key_prefix}/{team_side}/card.csv", Body=card_csv
    )
    log_messages.append(f"processed {team_side} team card table.")
    s3_client.put_object(
        Bucket=bucket, Key=f"{key_prefix}/{team_side}/sub.csv", Body=sub_csv
    )
    log_messages.append(f"processed {team_side} team sub table.")


def extract_summary(match_data, team_side):
    if team_side == "home":
        html_class = "event a"
    elif team_side == "away":
        html_class = "event b"
    raw_div = match_data.find_all("div", {"class": html_class})
    card_csv = "time,player,card\n"
    sub_csv = "time,player OUT,player IN\n"
    for event in raw_div:
        breakdown = [x.strip() for x in event.text.split("\n") if x.strip() != ""]
        time = breakdown[0].removesuffix("\u2019")
        event_type = breakdown[-1].removeprefix("\u2014\xa0")
        if event_type in ["Yellow Card", "Red Card", "Second Yellow Card"]:
            card_csv += f"{time},{breakdown[2]},{event_type}\n"
        elif event_type == "Substitute":
            sub_csv += f"{time},{breakdown[2]},{breakdown[3].removeprefix('for ')}\n"
    return card_csv, sub_csv
