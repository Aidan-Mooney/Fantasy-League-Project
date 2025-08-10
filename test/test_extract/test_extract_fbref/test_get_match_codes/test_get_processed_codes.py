from pytest import fixture
from os import environ
from unittest.mock import patch


from extract.extract_fbref.get_match_codes import get_processed_codes


MODULE_PATH = "extract.extract_fbref.get_match_codes"
TEST_BUCKET = "fixture-processing-tracker"


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
    environ["PROC_TRACK_BUCKET"] = TEST_BUCKET


@fixture(scope="function")
def s3_setup(s3_client):
    def _setup(keys):
        for key in keys:
            s3_client.put_object(Bucket=TEST_BUCKET, Key=key, Body="".encode("utf-8"))

    return _setup


def test_get_processed_codes_returns_list_of_strings(s3_setup):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_prefix = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/"
    test_keys = [f"{test_prefix}code1234.json"]
    s3_setup(test_keys)
    output = get_processed_codes(test_template, test_league, test_season)
    assert isinstance(output, list)
    for code in output:
        assert isinstance(code, str)


def test_get_processed_codes_returns_empty_list():
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    output = get_processed_codes(test_template, test_league, test_season)
    assert len(output) == 0


def test_get_processed_codes_returns_one_code(s3_setup):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_prefix = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/"
    test_keys = [f"{test_prefix}code1234.json"]
    s3_setup(test_keys)
    output = get_processed_codes(test_template, test_league, test_season)
    assert output == ["code1234"]


def test_get_processed_codes_returns_multiple_codes(s3_setup):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_prefix = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/"
    test_keys = [
        f"{test_prefix}code1234.json",
        f"{test_prefix}code5678.json",
        f"{test_prefix}code1011.json",
        f"{test_prefix}code1213.json",
    ]
    s3_setup(test_keys)
    output = get_processed_codes(test_template, test_league, test_season)
    assert set(output) == {"code1234", "code5678", "code1011", "code1213"}
