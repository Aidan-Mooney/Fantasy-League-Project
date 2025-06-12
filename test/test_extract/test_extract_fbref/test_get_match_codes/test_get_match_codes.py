from pytest import fixture
from unittest.mock import patch
from logging import CRITICAL, INFO
from requests.exceptions import HTTPError
from requests.models import Response
from botocore.exceptions import ClientError


from extract.extract_fbref.get_match_codes import get_match_codes


MODULE_PATH = "extract.extract_fbref.get_match_codes"


@fixture(scope="function")
def mock_get_fixtures():
    with (
        patch(f"{MODULE_PATH}.get_all_codes") as mock_get_all_codes,
        patch(f"{MODULE_PATH}.get_processed_codes") as mock_get_processed_code,
    ):
        yield mock_get_all_codes, mock_get_processed_code


class TestGetMatchCodesFunctionality:
    def test_get_match_codes_returns_correct_types(self, mock_get_fixtures):
        test_template = "template"
        test_league = "Premier-League"
        test_season = 2025
        mock_all_codes, mock_proc_codes = mock_get_fixtures
        mock_all_codes.return_value = ["code1234", "code5678"]
        mock_proc_codes.return_value = ["code1234"]
        test_event = {
            "template": test_template,
            "league": test_league,
            "season": test_season,
        }
        test_context = None
        result = get_match_codes(test_event, test_context)
        assert isinstance(result, dict)
        assert len(result) == 3
        assert isinstance(result["success"], bool)
        assert isinstance(result["links"], list)
        assert isinstance(result["count"], int)
        for link in result["links"]:
            assert isinstance(link, str)

    def test_get_match_codes_returns_empty_list_if_no_match_links_were_found(
        self,
        caplog,
        mock_get_fixtures,
    ):
        test_template = "template"
        test_league = "Premier-League"
        test_season = 2025
        mock_all_codes, mock_proc_codes = mock_get_fixtures
        mock_all_codes.return_value = []
        mock_proc_codes.return_value = []
        test_event = {
            "template": test_template,
            "league": test_league,
            "season": test_season,
        }
        test_context = None
        caplog.set_level(INFO)
        result = get_match_codes(test_event, test_context)
        assert result["success"]
        assert len(result["links"]) == 0
        assert result["count"] == 0
        assert (
            "Identified 0 new fixture links for league=Premier-League, season=2025"
            in caplog.text
        )

    def test_get_match_codes_returns_the_ouput_of_get_all_codes_if_bucket_is_empty(
        self,
        caplog,
        mock_get_fixtures,
    ):
        test_template = "template"
        test_league = "Premier-League"
        test_season = 2025
        mock_all_codes, mock_proc_codes = mock_get_fixtures
        mock_all_codes.return_value = ["code1234", "code5678"]
        mock_proc_codes.return_value = []
        test_event = {
            "template": test_template,
            "league": test_league,
            "season": test_season,
        }
        test_context = None
        caplog.set_level(INFO)
        result = get_match_codes(test_event, test_context)
        assert result["success"]
        assert set(result["links"]) == {"code1234", "code5678"}
        assert result["count"] == 2
        assert (
            "Identified 2 new fixture links for league=Premier-League, season=2025"
            in caplog.text
        )

    def test_get_match_codes_returns_only_codes_that_arent_in_bucket(
        self, caplog, mock_get_fixtures
    ):
        test_template = "template"
        test_league = "Premier-League"
        test_season = 2025
        mock_all_codes, mock_proc_codes = mock_get_fixtures
        mock_all_codes.return_value = ["code1234", "code5678", "code1011"]
        mock_proc_codes.return_value = ["code1234"]
        test_event = {
            "template": test_template,
            "league": test_league,
            "season": test_season,
        }
        test_context = None
        caplog.set_level(INFO)
        result = get_match_codes(test_event, test_context)
        assert result["success"]
        assert set(result["links"]) == {"code5678", "code1011"}
        assert result["count"] == 2
        assert (
            "Identified 2 new fixture links for league=Premier-League, season=2025"
            in caplog.text
        )


class TestGetMatchCodesLogsErrors:
    def test_get_match_codes_logs_an_invalid_event(self, caplog):
        test_event = {"invalid": "oh dear"}
        test_context = None
        caplog.set_level(CRITICAL)
        result = get_match_codes(test_event, test_context)
        assert not result["success"]
        assert len(result["links"]) == 0
        assert (
            result["error"]
            == "event must contain only the keys {'template', 'league', 'season'}"
        )
        assert (
            "Event validation failed: event must contain only the keys {'template', 'league', 'season'}"
            in caplog.text
        )

    def test_get_match_codes_logs_a_bad_http_request(self, caplog, mock_get_fixtures):
        test_template = "template"
        test_league = "Premier-League"
        test_season = 2025
        test_url = f"https://fbref.com/en/comps/9/{test_season - 1}-{test_season}/schedule/{test_season - 1}-{test_season}-{test_league}-Scores-and-Fixtures"
        mock_all_codes, _ = mock_get_fixtures
        response = Response()
        response.status_code = 403
        response.url = test_url
        response.reason = "Forbidden"
        error = HTTPError(
            f"403 Client Error: Forbidden for url: {response.url}", response=response
        )
        mock_all_codes.side_effect = error
        test_event = {
            "template": test_template,
            "league": test_league,
            "season": test_season,
        }
        test_context = None
        caplog.set_level(CRITICAL)
        result = get_match_codes(test_event, test_context)
        assert not result["success"]
        assert len(result["links"]) == 0
        assert result["error"] == f"403 Client Error: Forbidden for url: {test_url}"
        assert (
            "Failed to get fixture links for league=Premier-League, season=2025"
            in caplog.text
        )

    def test_get_match_codes_logs_a_s3_client_error(self, caplog, mock_get_fixtures):
        test_template = "template"
        test_league = "Premier-League"
        test_season = 2025
        mock_all_codes, mock_proc_codes = mock_get_fixtures
        error_response = {
            "Error": {
                "Code": "InternalServiceError",
                "Message": "An internal error occurred",
            },
            "ResponseMetadata": {"RequestId": "EXAMPLE123", "HTTPStatusCode": 500},
        }
        operation_name = "ListObjectsV2"
        error = ClientError(error_response, operation_name)
        mock_all_codes.return_value = ["code1234", "code5678", "code1011"]
        mock_proc_codes.side_effect = error
        test_event = {
            "template": test_template,
            "league": test_league,
            "season": test_season,
        }
        test_context = None
        caplog.set_level(CRITICAL)
        result = get_match_codes(test_event, test_context)
        assert not result["success"]
        assert len(result["links"]) == 0
        assert (
            result["error"]
            == "An error occurred (InternalServiceError) when calling the ListObjectsV2 operation: An internal error occurred"
        )
        assert (
            "Failed to fetch processed match codes for league=Premier-League, season=2025"
            in caplog.text
        )
