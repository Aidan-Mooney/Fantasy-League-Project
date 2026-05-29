from pytest import fixture
from unittest.mock import patch
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


def test_save_table_bytes_returns_none(s3_client, mock_log_json, extract_bucket_name):
    test_file_name = "file_name.csv"
    test_body = b"body"
    test_event_type = "table save"
    result = save_table_bytes(
        extract_bucket_name, test_file_name, test_body, test_event_type
    )
    assert result is None


def test_save_table_bytes_saves_correctly_and_logs_correctly_with_no_kwargs(
    s3_client, mock_log_json, extract_bucket_name
):
    test_file_name = "file_name.csv"
    test_body = b"body"
    test_event_type = "table save"
    save_table_bytes(extract_bucket_name, test_file_name, test_body, test_event_type)

    resp = s3_client.get_object(Bucket=extract_bucket_name, Key=test_file_name)
    assert resp["Body"].read() == test_body

    mock_log_json.assert_called_once()
    args, kwargs = mock_log_json.call_args
    msg = args[0]
    assert msg == "table save"
    assert kwargs["success"] is True
    assert kwargs["bytes"] == len(test_body)


def test_save_table_bytes_saves_correctly_and_logs_correctly_with_kwargs(
    s3_client, mock_log_json, extract_bucket_name
):
    test_file_name = "file_name.csv"
    test_body = b"body"
    test_event_type = "table save"
    test_kwarg = "kwarg"
    save_table_bytes(
        extract_bucket_name,
        test_file_name,
        test_body,
        test_event_type,
        test_kwarg=test_kwarg,
    )

    resp = s3_client.get_object(Bucket=extract_bucket_name, Key=test_file_name)
    assert resp["Body"].read() == test_body

    mock_log_json.assert_called_once()
    args, kwargs = mock_log_json.call_args
    msg = args[0]
    assert msg == "table save"
    assert kwargs["success"] is True
    assert kwargs["bytes"] == len(test_body)
    assert kwargs["test_kwarg"] == test_kwarg
