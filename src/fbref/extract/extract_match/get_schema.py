import json
from os import environ
from boto3 import client


s3_client = client("s3")


TEMPLATE_BUCKET = environ["TEMPLATE_BUCKET"]


def get_schema(template: str) -> dict:
    """
    Retrieve a JSON schema from S3 and return it as a dictionary.

    Args:
        template (str): The base name of the template file (without the `.json` extension).

    Returns:
        dict: The parsed JSON schema.

    Raises:
        ClientError: If the request to S3 fails (e.g. due to permission errors
            or network issues).

    Notes:
        This function assumes the template file exists in the configured bucket and is a valid json file.
        Existence and access checks should be handled prior to calling this function.
    """
    response = s3_client.get_object(Bucket=TEMPLATE_BUCKET, Key=f"{template}.json")
    return json.loads(response["Body"].read())
