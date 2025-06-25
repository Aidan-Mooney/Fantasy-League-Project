import json
from pytest import fixture
from unittest.mock import patch
from botocore.exceptions import ClientError
from logging import CRITICAL


from extract.extract_fbref.extract_template import extract_template


MODULE_PATH = "extract.extract_fbref.extract_template"
TEST_BUCKET = "template-bucket"


@fixture(autouse=True)
def patch_s3_client(s3_client):
    with patch(f"{MODULE_PATH}.s3_client", s3_client):
        yield


@fixture(autouse=True)
def create_bucket(s3_client):
    s3_client.create_bucket(
        Bucket=TEST_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@fixture(scope="function")
def s3_setup(s3_client):
    def _setup(key, body):
        s3_client.put_object(Bucket=TEST_BUCKET, Key=key, Body=body.encode("utf-8"))

    return _setup


@fixture(scope="function")
def mock_get_body():
    with patch(f"{MODULE_PATH}.get_body") as mock_get_body:
        yield mock_get_body


def test_extract_template_returns_correct_type(s3_setup):
    test_key = "test-template.json"
    test_json = {
        "Premier-League": {
            2025: {"schema": {}},
            2024: {"schema": {}},
            2023: {"schema": {}},
        }
    }
    body = json.dumps(test_json)
    s3_setup(test_key, body)

    test_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "2020-09-11T18:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": test_key, "size": 12345},
                },
            }
        ]
    }
    test_context = None

    result = extract_template(test_event, test_context)
    assert isinstance(result, dict)
    assert len(result) == 2
    assert isinstance(result["events"], list)
    assert isinstance(result["func_name"], str)


def test_extract_template_returns_one_event_with_one_league_and_one_season(s3_setup):
    test_key = "test-template.json"
    test_json = {
        "Premier-League": {
            2025: {"schema": {}},
        }
    }
    body = json.dumps(test_json)
    s3_setup(test_key, body)

    test_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "2020-09-11T18:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": test_key, "size": 12345},
                },
            }
        ]
    }
    test_context = None

    result = extract_template(test_event, test_context)
    assert result == {
        "events": [
            {"template": "test-template", "league": "Premier-League", "season": 2025}
        ],
        "func_name": "get_match_codes",
    }


def test_extract_template_returns_correctly_with_one_league_and_multiple_seasons(
    s3_setup,
):
    test_key = "test-template.json"
    test_json = {
        "Premier-League": {
            2025: {"schema": {}},
            2024: {"schema": {}},
            2023: {"schema": {}},
            2022: {"schema": {}},
        }
    }
    body = json.dumps(test_json)
    s3_setup(test_key, body)

    test_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "2020-09-11T18:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": test_key, "size": 12345},
                },
            }
        ]
    }
    test_context = None

    result = extract_template(test_event, test_context)
    assert result == {
        "events": [
            {"template": "test-template", "league": "Premier-League", "season": 2025},
            {"template": "test-template", "league": "Premier-League", "season": 2024},
            {"template": "test-template", "league": "Premier-League", "season": 2023},
            {"template": "test-template", "league": "Premier-League", "season": 2022},
        ],
        "func_name": "get_match_codes",
    }


def test_extract_template_returns_correctly_with_multiple_leagues_and_multiple_seasons(
    s3_setup,
):
    test_key = "test-template.json"
    test_json = {
        "Premier-League": {
            2025: {"schema": {}},
            2024: {"schema": {}},
            2023: {"schema": {}},
            2022: {"schema": {}},
        },
        "Serie-A": {
            2025: {"schema": {}},
            2024: {"schema": {}},
            2023: {"schema": {}},
            2022: {"schema": {}},
        },
        "Bundesliga": {
            2025: {"schema": {}},
            2024: {"schema": {}},
            2023: {"schema": {}},
            2022: {"schema": {}},
        },
    }
    body = json.dumps(test_json)
    s3_setup(test_key, body)

    test_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "2020-09-11T18:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": test_key, "size": 12345},
                },
            }
        ]
    }
    test_context = None

    result = extract_template(test_event, test_context)
    assert result == {
        "events": [
            {"template": "test-template", "league": "Premier-League", "season": 2025},
            {"template": "test-template", "league": "Premier-League", "season": 2024},
            {"template": "test-template", "league": "Premier-League", "season": 2023},
            {"template": "test-template", "league": "Premier-League", "season": 2022},
            {"template": "test-template", "league": "Serie-A", "season": 2025},
            {"template": "test-template", "league": "Serie-A", "season": 2024},
            {"template": "test-template", "league": "Serie-A", "season": 2023},
            {"template": "test-template", "league": "Serie-A", "season": 2022},
            {"template": "test-template", "league": "Bundesliga", "season": 2025},
            {"template": "test-template", "league": "Bundesliga", "season": 2024},
            {"template": "test-template", "league": "Bundesliga", "season": 2023},
            {"template": "test-template", "league": "Bundesliga", "season": 2022},
        ],
        "func_name": "get_match_codes",
    }


def test_extract_template_logs_client_errors(caplog, mock_get_body):
    mock_get_body_func = mock_get_body
    error_response = {
        "Error": {
            "Code": "InternalServiceError",
            "Message": "An internal error occurred",
        },
        "ResponseMetadata": {"RequestId": "EXAMPLE123", "HTTPStatusCode": 500},
    }
    operation_name = "SendMessage"
    error = ClientError(error_response, operation_name)
    mock_get_body_func.side_effect = error

    test_key = "test-template.json"
    test_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "2020-09-11T18:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": test_key, "size": 12345},
                },
            }
        ]
    }
    test_context = None
    caplog.set_level(CRITICAL)
    result = extract_template(test_event, test_context)
    assert not result["success"]

    error_message = "An error occurred (InternalServiceError) when calling the SendMessage operation: An internal error occurred"
    assert result["error"] == error_message
    assert (
        f"Failed to get key={test_key} from bucket={TEST_BUCKET} | Error: {error_message}"
        in caplog.text
    )
