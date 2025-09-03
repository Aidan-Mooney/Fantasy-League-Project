from pytest import fixture
from unittest.mock import patch
from datetime import datetime, timezone
from fbref.extract.save_table_bytes import save_table_bytes


MODULE_PATH = "fbref.extract.save_table_bytes"


@fixture(autouse=True)
def patch_s3_client(s3_client):
    with patch(f"{MODULE_PATH}.s3_client", s3_client):
        yield


@fixture(autouse=True)
def create_bucket(s3_client, extract_bucket_name):
    s3_client.create_bucket(
        Bucket=extract_bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@fixture(scope="function")
def mock_log_json():
    with patch(f"{MODULE_PATH}.log_json") as mock:
        yield mock


@fixture(scope="function")
def mock_datetime_now():
    with patch(f"{MODULE_PATH}.datetime") as mock_dt:
        mock_now = datetime(2025, 9, 2, 12, 0, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = mock_now
        mock_dt.timezone = timezone
        yield mock_dt


def test_save_table_bytes_returns_none(
    s3_client, mock_log_json, mock_datetime_now, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_side = "home"
    test_table_name = "shots"
    test_body = b"body"
    result = save_table_bytes(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_side,
        test_table_name,
        test_body,
    )
    assert result is None


def test_save_table_bytes_saves_correctly_and_logs_correctly_with_home_team(
    s3_client, mock_log_json, mock_datetime_now, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_side = "home"
    test_table_name = "shots"
    test_body = "body".encode("utf-8")
    save_table_bytes(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_side,
        test_table_name,
        test_body,
    )

    key_expected = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_side}/{test_table_name}.csv"

    resp = s3_client.get_object(Bucket=extract_bucket_name, Key=key_expected)
    assert resp["Body"].read() == test_body

    mock_log_json.assert_called_once()
    args, kwargs = mock_log_json.call_args
    msg, log_dict = args
    assert msg == "table event"
    assert log_dict["event"] == "table_saved"
    assert log_dict["bucket"] == extract_bucket_name
    assert log_dict["template"] == test_template
    assert log_dict["league"] == test_league
    assert log_dict["season"] == test_season
    assert log_dict["fixture_id"] == test_fixture_id
    assert log_dict["table_name"] == test_table_name
    assert log_dict["team_side"] == test_side
    assert log_dict["key"] == key_expected
    assert log_dict["bytes"] == len(test_body)
    assert log_dict["time"] == datetime(
        2025, 9, 2, 12, 0, 0, tzinfo=timezone.utc
    ).isoformat(timespec="milliseconds")


def test_save_table_bytes_saves_ands_logs_correctly_with_no_side(
    s3_client, mock_log_json, mock_datetime_now, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_side = None
    test_table_name = "shots"
    test_body = b"body"

    key_expected = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_table_name}.csv"

    save_table_bytes(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_side,
        test_table_name,
        test_body,
    )

    resp = s3_client.get_object(Bucket=extract_bucket_name, Key=key_expected)
    assert resp["Body"].read() == test_body

    mock_log_json.assert_called_once()
    args, kwargs = mock_log_json.call_args
    msg, log_dict = args
    assert msg == "table event"
    assert log_dict["event"] == "table_saved"
    assert log_dict["bucket"] == extract_bucket_name
    assert log_dict["template"] == test_template
    assert log_dict["league"] == test_league
    assert log_dict["season"] == test_season
    assert log_dict["fixture_id"] == test_fixture_id
    assert log_dict["table_name"] == test_table_name
    assert "team_side" not in log_dict
    assert log_dict["key"] == key_expected
    assert log_dict["bytes"] == len(test_body)
    assert log_dict["time"] == datetime(
        2025, 9, 2, 12, 0, 0, tzinfo=timezone.utc
    ).isoformat(timespec="milliseconds")
