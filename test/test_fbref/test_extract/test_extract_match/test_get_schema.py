from pytest import fixture
from unittest.mock import patch
import json
from fbref.extract.extract_match.get_schema import get_schema


MODULE_PATH = "fbref.extract.extract_match.get_schema"


@fixture(autouse=True)
def patch_s3_client(s3_client):
    with patch(f"{MODULE_PATH}.s3_client", s3_client):
        yield


@fixture(autouse=True)
def create_bucket(s3_client, template_bucket_name):
    s3_client.create_bucket(
        Bucket=template_bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@fixture(scope="function")
def s3_setup(s3_client, template_bucket_name):
    def _setup(key, body):
        s3_client.put_object(
            Bucket=template_bucket_name, Key=key + ".json", Body=body.encode("utf-8")
        )

    return _setup


def test_get_schema_returns_a_dictionary(s3_setup):
    test_template = "test_template"
    test_schema = {"test": ["a", "b"]}
    test_body = json.dumps(test_schema)
    s3_setup(test_template, test_body)
    result = get_schema(test_template)
    assert isinstance(result, dict)


def test_get_schema_returns_the_schema_from_the_template_bucket(s3_client, s3_setup):
    test_template = "test_template"
    test_schema = {"test": ["a", "b"]}
    test_body = json.dumps(test_schema)
    s3_setup(test_template, test_body)
    result = get_schema(test_template)
    assert result == test_schema
