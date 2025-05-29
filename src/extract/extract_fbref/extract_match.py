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


def html_table_to_csv_string(table):
    header_rows = table.find("thead").find_all("tr")

    if len(header_rows) == 1:
        headers = [th.get_text(strip=True) for th in header_rows[0].find_all("th")]
    else:
        top_row = header_rows[0]
        bottom_row = header_rows[1]

        expanded_top = []
        for th in top_row.find_all("th"):
            colspan = int(th.get("colspan", 1))
            text = th.get_text(strip=True)
            expanded_top.extend([text] * colspan)

        bottom = [th.get_text(strip=True) for th in bottom_row.find_all("th")]

        headers = [
            f"{top} {bottom}".strip() if top else bottom
            for top, bottom in zip(expanded_top, bottom)
        ]
    csv_string = ",".join(headers) + "\n"
    for tr in table.find_all("tbody")[0].find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row = [cell.get_text(strip=True) for cell in cells]
        if row:
            csv_string += ",".join(row) + "\n"
    return csv_string


def process_match_summary(soup):
    extract_bucket = environ["EXTRACT_BUCKET"]
    return
