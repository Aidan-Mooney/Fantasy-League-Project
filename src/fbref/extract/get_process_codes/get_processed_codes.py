from os import environ
from boto3 import client
from typing import List


s3_client = client("s3")


def get_processed_codes(template: str, league: str, season: int) -> List[str]:
    """
    Retrieve processed match codes from an S3 bucket.

    This function queries the configured S3 bucket for objects stored under the
    path corresponding to the given template, league, and season. It returns
    the list of match codes by stripping the S3 key prefix and the `.json`
    extension from each object key.

    Args:
        template (str): The S3 path prefix for the data (e.g. "matches").
        league (str): The league identifier (e.g. "Premier-League").
        season (int): The ending year of the season (e.g. 2024 for the 2023–24 season).

    Returns:
        List[str]: A list of processed match codes without file extensions.

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        - The target S3 bucket name is read from the environment variable
          `PROC_TRACK_BUCKET`.
        - The S3 prefix follows the format:
          ``"{template}/{league}/{season-1}-{season}/"``.
    """
    prefix = f"{template}/{league}/{season - 1}-{season}/"
    bucket = environ["PROC_TRACK_BUCKET"]

    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    keys = [obj["Key"] for obj in response.get("Contents", [])]
    codes = [key.removeprefix(prefix).removesuffix(".json") for key in keys]
    return codes
