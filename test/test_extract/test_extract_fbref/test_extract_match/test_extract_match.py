from os import environ
import json
from bs4 import BeautifulSoup
from pytest import fixture
from unittest.mock import patch
from logging import CRITICAL
from requests.exceptions import HTTPError
from botocore.exceptions import ClientError


from extract.extract_fbref.extract_match import extract_match


MODULE_PATH = "extract.extract_fbref.extract_match"
PROC_TRACK_BUCKET = "proc-track-bucket"
EXTACT_BUCKET = "extract-bucket"
TEMPLATE_BUCKET = "template-bucket"
TEST_TEMPLATE = "test_template"


environ["PROC_TRACK_BUCKET"] = PROC_TRACK_BUCKET
environ["EXTRACT_BUCKET"] = EXTACT_BUCKET
environ["TEMPLATE_BUCKET"] = TEMPLATE_BUCKET


@fixture(autouse=True)
def patch_s3_client(s3_client):
    with patch(f"{MODULE_PATH}.s3_client", s3_client):
        yield


@fixture(autouse=True)
def create_buckets(s3_client):
    s3_client.create_bucket(
        Bucket=PROC_TRACK_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.create_bucket(
        Bucket=EXTACT_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.create_bucket(
        Bucket=TEMPLATE_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@fixture(autouse=True)
def template_json(s3_client):
    test_json = {"test": "test"}
    body = json.dumps(test_json)
    s3_client.put_object(Bucket=TEMPLATE_BUCKET, Key=f"{TEST_TEMPLATE}.json", Body=body)


@fixture(scope="function")
def mock_processes():
    with (
        patch(f"{MODULE_PATH}.process_match_tables") as mock_process_match_tables,
        patch(f"{MODULE_PATH}.process_match_summary") as mock_process_match_summary,
    ):
        yield mock_process_match_tables, mock_process_match_summary


class TestExtractMatchFunctionality:
    def test_extract_match_returns_correct_types(
        self, mock_requests_get, mock_processes
    ):
        test_template = TEST_TEMPLATE
        test_league = "Premier-League"
        test_season = 2025
        fixture_id = "12345678"
        test_event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "template": test_template,
                            "league": test_league,
                            "season": test_season,
                            "fixture_id": fixture_id,
                        }
                    )
                }
            ]
        }
        test_context = None
        result = extract_match(test_event, test_context)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert "success" in result
        assert isinstance(result["success"], bool)

    def test_extract_match_on_success_will_record_code_in_the_tracker(
        self, mock_requests_get, mock_processes, s3_client
    ):
        test_template = TEST_TEMPLATE
        test_league = "Premier-League"
        test_season = 2025
        fixture_id = "12345678"
        test_event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "template": test_template,
                            "league": test_league,
                            "season": test_season,
                            "fixture_id": fixture_id,
                        }
                    )
                }
            ]
        }
        test_context = None
        extract_match(test_event, test_context)
        expected_prefix = (
            f"{test_template}/{test_league}/{test_season - 1}-{test_season}"
        )
        expected_key = f"{expected_prefix}/{fixture_id}.json"
        response = s3_client.list_objects_v2(Bucket=PROC_TRACK_BUCKET)
        keys = [obj["Key"] for obj in response.get("Contents", [])]
        assert expected_key in keys

    def test_extract_match_triggers_the_two_processes(
        self, mock_requests_get, mock_processes
    ):
        mock_pmt, mock_pms = mock_processes

        test_template = TEST_TEMPLATE
        test_league = "Premier-League"
        test_season = 2025
        fixture_id = "12345678"
        test_event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "template": test_template,
                            "league": test_league,
                            "season": test_season,
                            "fixture_id": fixture_id,
                        }
                    )
                }
            ]
        }
        test_context = None
        extract_match(test_event, test_context)

        test_prefix = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{fixture_id}"

        assert mock_pmt.call_count == 1
        pmt_args, pmt_kwargs = mock_pmt.call_args
        assert pmt_args == (EXTACT_BUCKET, test_prefix, [], {"test": "test"}, [])
        assert len(pmt_kwargs) == 0

        assert mock_pms.call_count == 1
        pms_args, pms_kwargs = mock_pms.call_args
        assert pms_args == (
            EXTACT_BUCKET,
            test_prefix,
            BeautifulSoup("<html><b><h1>Default Page</h1></b></html>", "html.parser"),
            [],
        )
        assert len(pms_kwargs) == 0


class TestGetMatchCodesLogsErrors:
    def test_extract_match_logs_an_invalid_event(self, caplog):
        test_event = {"Records": [{"body": json.dumps({"invalid": "oh dear"})}]}
        test_context = None
        caplog.set_level(CRITICAL)
        result = extract_match(test_event, test_context)
        assert not result["success"]
        assert (
            result["error"]
            == "event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
        )
        assert (
            "Event validation failed: event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
            in caplog.text
        )

    def test_extract_match_logs_a_bad_http_request(
        self, caplog, mock_requests_get, mock_processes
    ):
        test_template = TEST_TEMPLATE
        test_league = "Premier-League"
        test_season = 2025
        fixture_id = "12345678"

        _, mock_response = mock_requests_get
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError(
            "404 Client Error: Not Found"
        )

        test_event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "template": test_template,
                            "league": test_league,
                            "season": test_season,
                            "fixture_id": fixture_id,
                        }
                    )
                }
            ]
        }
        test_context = None

        caplog.set_level(CRITICAL)
        result = extract_match(test_event, test_context)
        assert not result["success"]
        assert result["error"] == "404 Client Error: Not Found"
        assert (
            "Failed to retrieve soup for league=Premier-League, season=2025, fixture_id=12345678"
            in caplog.text
        )

    def test_extract_match_logs_a_s3_client_error(
        self, caplog, mock_requests_get, mock_processes
    ):
        mock_pmt, _ = mock_processes
        error_response = {
            "Error": {
                "Code": "InternalServiceError",
                "Message": "An internal error occurred",
            },
            "ResponseMetadata": {"RequestId": "EXAMPLE123", "HTTPStatusCode": 500},
        }
        operation_name = "PutObject"
        error = ClientError(error_response, operation_name)
        mock_pmt.side_effect = error

        test_template = TEST_TEMPLATE
        test_league = "Premier-League"
        test_season = 2025
        fixture_id = "12345678"
        test_event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "template": test_template,
                            "league": test_league,
                            "season": test_season,
                            "fixture_id": fixture_id,
                        }
                    )
                }
            ]
        }
        test_context = None

        caplog.set_level(CRITICAL)
        result = extract_match(test_event, test_context)
        assert not result["success"]
        assert (
            result["error"]
            == "An error occurred (InternalServiceError) when calling the PutObject operation: An internal error occurred"
        )
        assert (
            "Failed to put match data for template=test_template, league=Premier-League, season=2025, fixture_id=12345678"
            in caplog.text
        )
