from pytest import fixture
from unittest.mock import patch
from bs4 import BeautifulSoup


from extract.extract_fbref.extract_match import process_table


MODULE_PATH = "extract.extract_fbref.extract_match"
TEST_BUCKET = "extract-bucket"


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
def soup_input_helper():
    def _setup(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("table")

    return _setup


def test_process_table_returns_none(soup_input_helper):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    test_table_name = "test table"
    team_side = "home"
    input_html = f"""
    <table>
        <caption>{test_team_name} {test_table_name}</caption>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
            <tr><td>Row2A</td><td>Row2B</td></tr>
        </tbody>
    </table>
    """
    test_table = soup_input_helper(input_html)
    test_schema = {"test_table": ["ColA", "ColB"]}
    log_messages = []
    result = process_table(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_name,
        test_table,
        test_schema,
        log_messages,
    )
    assert result is None


def test_process_table_does_nothing_if_the_table_name_is_not_in_the_schema(
    soup_input_helper, s3_client
):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    test_table_name = "test table"
    team_side = "home"
    input_html = f"""
    <table>
        <caption>{test_team_name} {test_table_name}</caption>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
            <tr><td>Row2A</td><td>Row2B</td></tr>
        </tbody>
    </table>
    """
    test_table = soup_input_helper(input_html)
    test_schema = {"another table": ["ColA", "ColB"]}
    log_messages = []
    process_table(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_name,
        test_table,
        test_schema,
        log_messages,
    )

    assert f"processed {team_side} team {test_table_name} table." not in log_messages
    response = s3_client.list_objects_v2(Bucket=TEST_BUCKET)
    keys = [obj["Key"] for obj in response.get("Contents", [])]
    assert f"{test_prefix}/{team_side}/{test_table_name}.csv" not in keys


def test_process_table_puts_table_and_logs_messages(soup_input_helper, s3_client):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    test_table_name = "test table"
    team_side = "home"
    input_html = f"""
    <table>
        <caption>{test_team_name} {test_table_name}</caption>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
            <tr><td>Row2A</td><td>Row2B</td></tr>
        </tbody>
    </table>
    """
    test_table = soup_input_helper(input_html)
    test_schema = {"test table": ["ColA", "ColB"]}
    log_messages = []
    process_table(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_name,
        test_table,
        test_schema,
        log_messages,
    )
    expected_table = "ColA,ColB\n" + "Row1A,Row1B\n" + "Row2A,Row2B\n"

    assert f"processed {team_side} team {test_table_name} table." in log_messages
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/{team_side}/{test_table_name}.csv"
    )
    assert response["Body"].read().decode("utf-8") == expected_table


def test_process_table_puts_table_with_specific_columns_and_logs_messages(
    soup_input_helper, s3_client
):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    test_table_name = "test table"
    team_side = "home"
    input_html = f"""
    <table>
        <caption>{test_team_name} {test_table_name}</caption>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
            <tr><td>Row2A</td><td>Row2B</td></tr>
        </tbody>
    </table>
    """
    test_table = soup_input_helper(input_html)
    test_schema = {"test table": ["ColA"]}
    log_messages = []
    process_table(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_name,
        test_table,
        test_schema,
        log_messages,
    )
    expected_table = "ColA\n" + "Row1A\n" + "Row2A\n"

    assert f"processed {team_side} team {test_table_name} table." in log_messages
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/{team_side}/{test_table_name}.csv"
    )
    assert response["Body"].read().decode("utf-8") == expected_table
