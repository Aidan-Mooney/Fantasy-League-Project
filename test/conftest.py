from pytest import fixture
from os import environ
from unittest.mock import patch, Mock
from boto3 import client
from moto import mock_aws


@fixture(scope="function")
def aws_credentials():
    environ["AWS_ACCESS_KEY_ID"] = "test"
    environ["AWS_SECRET_ACCESS_KEY"] = "test"
    environ["AWS_SECURITY_TOKEN"] = "test"
    environ["AWS_SESSION_TOKEN"] = "test"
    environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@fixture(scope="function")
def s3_client(aws_credentials):
    with mock_aws():
        yield client("s3", region_name="eu-west-2")


@fixture
def mock_requests_get():
    with patch("src.shared_utils.get_soup.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><b><h1>Default Page</h1></b></html>"

        mock_get.return_value = mock_response
        yield mock_get, mock_response
