import re
from os import environ
from boto3 import client


from get_soup import get_soup


s3_client = client("s3")


def extract_match(event, context):
    process_tracking_bucket = environ["PROC_TRACK_BUCKET"]
    extract_bucket = environ["EXTRACT_BUCKET"]
    template = event["template"]
    league = event["league"]
    season = event["season"]
    fixture_id = event["fixture_id"]
    url = f"https://fbref.com/en/matches/{fixture_id}"
    soup = get_soup(url)
    raw_html_tables = soup.find_all(lambda tag: tag.name == "table")
    process_match_tables(extract_bucket, raw_html_tables)
    process_match_summary(extract_bucket, soup)
    client.put_object(
        Bucket=process_tracking_bucket,
        Key=f"{template}{league}/{season - 1}-{season}/{fixture_id}.json",
        Body="",
    )
    return {}


def process_match_tables(bucket, raw_html_tables, table_schema: dict):
    home_team, home_formation, home_starters, home_bench = process_lineup_data(
        raw_html_tables[0]
    )
    away_team, away_formation, away_starters, away_bench = process_lineup_data(
        raw_html_tables[1]
    )
    for table in raw_html_tables[2:]:
        caption = table.find("caption")
        table_name = caption.get_text(strip=True) if caption else "Unnamed Table"
        csv = html_table_to_csv_string(table)
    return


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


def process_match_summary(bucket, soup):
    return
