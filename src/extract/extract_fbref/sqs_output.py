from os import environ
import json
import boto3
from logging import getLogger, basicConfig, INFO
from botocore.exceptions import ClientError


basicConfig(level=INFO)
logger = getLogger(__name__)
sqs_client = boto3.client("sqs")


def sqs_output(event, context):
    QUEUE = environ["FBREF_QUEUE"]
    try:
        return_event = receive_message(QUEUE)
    except ClientError as err:
        logger.critical(
            "Failed to receive item from the queue=%s. Error: %s",
            QUEUE,
            err,
        )
        return {"success": False, "error": str(err)}
    return return_event


def receive_message(queue):
    response = sqs_client.receive_message(
        QueueUrl=queue,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5,
        MessageAttributeNames=["All"],
    )

    messages = response.get("Messages", [])
    if not messages:
        return {"event": None, "func_name": None, "is_finished": True}

    message = messages[0]
    sqs_client.delete_message(QueueUrl=queue, ReceiptHandle=message["ReceiptHandle"])

    return_info = json.loads(message["Body"])
    return_info["is_finished"] = False
    return return_info
