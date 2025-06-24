from os import environ
import json
import boto3
from logging import getLogger, basicConfig, INFO
from botocore.exceptions import ClientError


basicConfig(level=INFO)
logger = getLogger(__name__)


def get_sqs_client():
    return boto3.client("sqs")


def sqs_input(event, context):
    try:
        validate_event(event)
    except TypeError as err:
        logger.critical("Event validation failed: %s | Event: %s", err, event)
        return {"success": False, "error": str(err)}

    QUEUE = environ["FBREF_QUEUE"]
    events = event["events"]
    func_name = event["func_name"]

    for event_input in events:
        try:
            queue_event(QUEUE, func_name, event_input)
            logger.info(
                "Added event=%s for func=%s to the queue.",
                event_input,
                func_name,
            )
        except ClientError as err:
            logger.critical(
                "Failed to add event=%s for func=%s to the queue=%s. Error: %s",
                event_input,
                func_name,
                QUEUE,
                err,
            )
            return {"success": False, "error": str(err)}

    return {"success": True}


def validate_event(event):
    expected_keys = {"events", "func_name"}
    if not isinstance(event, dict):
        raise TypeError("event must be a dictionary")
    actual_keys = set(event.keys())
    if actual_keys != expected_keys:
        raise TypeError("event must contain only the keys {'events', 'func_name'}")
    elif not isinstance(event["events"], list):
        raise TypeError("events value must be a list")
    elif not isinstance(event["func_name"], str):
        raise TypeError("func_name value must be a string")


def queue_event(queue, func_name, event):
    sqs_client = get_sqs_client()
    output_event = {
        "func_name": func_name,
        "event": event,
    }
    sqs_client.send_message(
        QueueUrl=queue,
        MessageBody=json.dumps(output_event),
        MessageGroupId="fbref-extract",
    )
