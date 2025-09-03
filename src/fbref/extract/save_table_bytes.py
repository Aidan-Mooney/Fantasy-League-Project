from boto3 import client
from datetime import datetime, timezone
from fbref.extract.log_json import log_json


s3_client = client("s3")


def save_table_bytes(
    bucket, template, league, season, fixture_id, team_side, table_name, body
):
    prefix = f"{template}/{league}/{season - 1}-{season}/{fixture_id}"
    log_dict = {
        "event": "table_saved",
        "bucket": bucket,
        "template": template,
        "league": league,
        "season": season,
        "fixture_id": fixture_id,
        "table_name": table_name,
        "bytes": len(body),
    }
    if team_side is not None:
        key = f"{prefix}/{team_side}/{table_name}.csv"
        log_dict["team_side"] = team_side
        log_dict["key"] = key
    else:
        key = f"{prefix}/{table_name}.csv"
        log_dict["key"] = key

    s3_client.put_object(Bucket=bucket, Key=key, Body=body)

    log_dict["time"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    log_json("table event", log_dict)
