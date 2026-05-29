from boto3 import client
from fbref.extract.log_json import log_json


s3_client = client("s3")


def save_table_bytes(
    bucket: str, file_name: str, body: bytes, event_type: str, **log_info: str | int
) -> None:
    """
    Save raw bytes to an S3 bucket and log details about the save event.

    Args:
        bucket (str): The name of the destination S3 bucket.
        file_name (str): The key (file name) under which the object will be stored.
        body (bytes): The content to upload.
        event_type (str): A label describing the type of event (e.g., "table_save").

    Keyword Args:
        **log_info: Additional metadata to include in the log (e.g., timestamp as str,
            season as int).

    Returns:
        None

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        This function enriches the provided ``log_info`` with two extra fields:
        - ``bytes``: The size of the uploaded object in bytes.
        - ``success``: Boolean flag indicating upload success.
    """
    s3_client.put_object(Bucket=bucket, Key=file_name, Body=body)
    log_info["bytes"] = len(body)
    log_info["success"] = True
    log_json(event_type, **log_info)
