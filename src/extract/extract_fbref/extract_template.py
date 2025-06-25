import json
from boto3 import client
from logging import getLogger, basicConfig, INFO
from botocore.exceptions import ClientError


basicConfig(level=INFO)
logger = getLogger(__name__)
s3_client = client("s3")


def extract_template(event, context):
    s3_object = event["Records"][0]["s3"]
    bucket = s3_object["bucket"]["name"]
    key = s3_object["object"]["key"]

    try:
        template_info = get_body(bucket, key)
    except ClientError as err:
        logger.critical(
            "Failed to get key=%s from bucket=%s | Error: %s", key, bucket, err
        )
        return {"success": False, "error": str(err)}

    template_name = key.removesuffix(".json")
    return {
        "events": [
            {"template": template_name, "league": league, "season": int(season)}
            for league in template_info
            for season in template_info[league]
        ],
        "func_name": "get_match_codes",
    }


def get_body(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return json.load(response["Body"])
