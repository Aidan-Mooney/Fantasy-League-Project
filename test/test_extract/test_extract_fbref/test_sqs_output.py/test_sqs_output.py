from pytest import fixture
from os import environ
from unittest.mock import patch
import json
from botocore.exceptions import ClientError
from logging import CRITICAL


from extract.extract_fbref.sqs_output import sqs_output


MODULE_PATH = "extract.extract_fbref.sqs_output"
TEST_QUEUE = "test-queue.fifo"


@fixture(autouse=True)
def patch_s3_client(sqs_client):
    with patch(f"{MODULE_PATH}.sqs_client", sqs_client):
        yield


@fixture(autouse=True)
def create_queue(sqs_client):
    sqs_client.create_queue(
        QueueName=TEST_QUEUE,
        Attributes={"FifoQueue": "true", "ContentBasedDeduplication": "true"},
    )
    environ["FBREF_QUEUE"] = TEST_QUEUE


@fixture(scope="function")
def add_messages(sqs_client):
    def _setup(events, func_name):
        for event in events:
            output_event = {
                "func_name": func_name,
                "event": event,
            }
            sqs_client.send_message(
                QueueUrl=TEST_QUEUE,
                MessageBody=json.dumps(output_event),
                MessageGroupId="fbref-extract",
            )

    return _setup


@fixture(scope="function")
def mock_receive_message():
    with patch(f"{MODULE_PATH}.receive_message") as mock_receive_message_func:
        yield mock_receive_message_func


def test_sqs_output_returns_a_dict_with_an_event_func_name_and_is_finished_bool(
    add_messages,
):
    events_list = [{"test": "test"}]
    test_func_name = "test_function"
    add_messages(events_list, test_func_name)
    test_event = {}
    test_context = None
    result = sqs_output(test_event, test_context)
    assert isinstance(result, dict)
    assert len(result) == 3
    assert "event" in result
    assert "func_name" in result
    assert "is_finished" in result
    assert isinstance(result["event"], dict)
    assert isinstance(result["func_name"], str)
    assert isinstance(result["is_finished"], bool)


def test_sqs_output_returns_empty_event_and_func_name_with_true_is_finished():
    test_event = {}
    test_context = None
    result = sqs_output(test_event, test_context)
    assert result["event"] is None
    assert result["func_name"] is None
    assert result["is_finished"] is True


def test_sqs_output_gets_the_func_and_event_from_queue_with_one_message(add_messages):
    events_list = [{"test": "test"}]
    test_func_name = "test_function"
    add_messages(events_list, test_func_name)
    test_event = {}
    test_context = None
    result = sqs_output(test_event, test_context)
    assert result["event"] == {"test": "test"}
    assert result["func_name"] == "test_function"
    assert result["is_finished"] is False


def test_sqs_output_gets_the_first_event_and_func_with_multiple_messages_in_queue(
    add_messages,
):
    events_list = [
        {"test": "test1"},
        {"test": "test2"},
        {"test": "test3"},
        {"test": "test4"},
    ]
    test_func_name = "test_function"
    add_messages(events_list, test_func_name)
    test_event = {}
    test_context = None
    result = sqs_output(test_event, test_context)
    assert result["event"] == {"test": "test1"}
    assert result["func_name"] == "test_function"
    assert result["is_finished"] is False


def test_sqs_output_logs_client_errors(caplog, mock_receive_message):
    mock_receive_message_func = mock_receive_message
    error_response = {
        "Error": {
            "Code": "InternalServiceError",
            "Message": "An internal error occurred",
        },
        "ResponseMetadata": {"RequestId": "EXAMPLE123", "HTTPStatusCode": 500},
    }
    operation_name = "SendMessage"
    error = ClientError(error_response, operation_name)
    mock_receive_message_func.side_effect = error

    test_event = {}
    test_context = None
    caplog.set_level(CRITICAL)
    result = sqs_output(test_event, test_context)
    assert not result["success"]

    error_message = "An error occurred (InternalServiceError) when calling the SendMessage operation: An internal error occurred"
    assert result["error"] == error_message
    assert (
        f"Failed to receive item from the queue={TEST_QUEUE}. Error: {error_message}"
        in caplog.text
    )
