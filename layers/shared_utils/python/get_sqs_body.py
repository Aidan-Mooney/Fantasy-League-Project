import json


def get_sqs_body(event):
    return [json.loads(response["body"]) for response in event["Records"]]
