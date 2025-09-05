import json
from os import environ
from boto3 import client


s3_client = client("s3")


TEMPLATE_BUCKET = environ["TEMPLATE_BUCKET"]


def get_schema(template):
    response = s3_client.get_object(Bucket=TEMPLATE_BUCKET, Key=f"{template}.json")
    return json.loads(response["Body"].read())
