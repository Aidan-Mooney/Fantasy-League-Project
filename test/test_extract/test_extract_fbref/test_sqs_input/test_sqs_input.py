from pytest import fixture
from os import environ
from unittest.mock import patch
from botocore.exceptions import ClientError
from logging import CRITICAL, INFO


from extract.extract_fbref.sqs_input import sqs_input


MODULE_PATH = "extract.extract_fbref.sqs_input"
TEST_QUEUE = "test-queue.fifo"


@fixture(autouse=True)
def patch_s3_client(sqs_client):
    with patch(f"{MODULE_PATH}.get_sqs_client", return_value=sqs_client):
        yield


@fixture(autouse=True)
def create_queue(sqs_client):
    sqs_client.create_queue(
        QueueName=TEST_QUEUE,
        Attributes={"FifoQueue": "true", "ContentBasedDeduplication": "true"},
    )
    environ["FBREF_QUEUE"] = TEST_QUEUE


@fixture(scope="function")
def mock_queue_event():
    with patch(f"{MODULE_PATH}.queue_event") as mock_queue_event_func:
        yield mock_queue_event_func


def test_sqs_input_returns_success_dict():
    test_events = [{"test": "event"}, {"test": "another"}]
    test_func = "test_func"
    test_event = {"events": test_events, "func_name": test_func}
    test_context = None
    result = sqs_input(test_event, test_context)
    assert isinstance(result, dict)
    assert "success" in result
    assert isinstance(result["success"], bool)


def test_sqs_input_can_add_one_event_to_queue(caplog, sqs_client):
    test_events = [{"test": "event"}]
    test_func = "test_func"
    test_event = {"events": test_events, "func_name": test_func}
    test_context = None
    caplog.set_level(INFO)
    result = sqs_input(test_event, test_context)
    assert result["success"]
    messages = sqs_client.receive_message(QueueUrl=TEST_QUEUE, MaxNumberOfMessages=10)
    assert len(messages.get("Messages", [])) == len(test_events)
    assert (
        f"Added event={test_events[0]} for func={test_func} to the queue."
        in caplog.text
    )


def test_sqs_input_can_add_multiple_events_to_queue(caplog, sqs_client):
    test_events = [
        {"test": "event1"},
        {"test": "event2"},
        {"test": "event3"},
        {"test": "event4"},
        {"test": "event5"},
    ]
    test_func = "test_func"
    test_event = {"events": test_events, "func_name": test_func}
    test_context = None
    caplog.set_level(INFO)
    result = sqs_input(test_event, test_context)
    assert result["success"]
    messages = sqs_client.receive_message(QueueUrl=TEST_QUEUE, MaxNumberOfMessages=10)
    assert len(messages.get("Messages", [])) == len(test_events)
    for event in test_events:
        assert f"Added event={event} for func={test_func} to the queue." in caplog.text


def test_get_match_codes_logs_an_invalid_event(caplog):
    test_event = {"invalid": "oh dear"}
    test_context = None
    caplog.set_level(CRITICAL)
    result = sqs_input(test_event, test_context)
    assert not result["success"]
    assert result["error"] == "event must contain only the keys {'events', 'func_name'}"
    assert (
        "Event validation failed: event must contain only the keys {'events', 'func_name'}"
        in caplog.text
    )


def test_sqs_input_logs_client_errors(caplog, mock_queue_event):
    mock_queue_event_func = mock_queue_event
    error_response = {
        "Error": {
            "Code": "InternalServiceError",
            "Message": "An internal error occurred",
        },
        "ResponseMetadata": {"RequestId": "EXAMPLE123", "HTTPStatusCode": 500},
    }
    operation_name = "SendMessage"
    error = ClientError(error_response, operation_name)
    mock_queue_event_func.side_effect = error

    test_events = [
        {"test": "event1"},
        {"test": "event2"},
        {"test": "event3"},
        {"test": "event4"},
        {"test": "event5"},
    ]
    test_func = "test_func"
    test_event = {"events": test_events, "func_name": test_func}
    test_context = None
    caplog.set_level(CRITICAL)
    result = sqs_input(test_event, test_context)
    assert not result["success"]

    error_message = "An error occurred (InternalServiceError) when calling the SendMessage operation: An internal error occurred"
    assert result["error"] == error_message
    assert (
        f"Failed to add event={test_events[0]} for func={test_func} to the queue={TEST_QUEUE}. Error: {error_message}"
        in caplog.text
    )
