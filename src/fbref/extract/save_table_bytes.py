from boto3 import client
from fbref.extract.log_json import log_json


s3_client = client("s3")


def save_table_bytes(bucket, file_name, body, event_type, **log_info):
    s3_client.put_object(Bucket=bucket, Key=file_name, Body=body)
    log_info["bytes"] = len(body)
    log_info["success"] = True
    log_json(event_type, log_info)
