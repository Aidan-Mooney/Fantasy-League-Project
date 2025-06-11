from pytest import fixture
from unittest.mock import patch
from bs4 import BeautifulSoup


from extract.extract_fbref.extract_match import process_team_tables, table_name_dict


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
def table_generator():
    def _setup(number):
        html_string = ""
        for i in range(number):
            html_string += f"""
            <table>
                <thead>
                    <tr><th>ColA{i}</th><th>ColB{i}</th></tr>
                </thead>
                <tbody>
                    <tr><td>Row1A{i}</td><td>Row1B{i}</td></tr>
                    <tr><td>Row2A{i}</td><td>Row2B{i}</td></tr>
                </tbody>
            </table>
            """
        soup = BeautifulSoup(html_string, "html.parser")
        return soup.find_all("table")

    return _setup


def test_process_team_tables_returns_none():
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    test_formation = "4-2-3-1"
    test_starters = [
        ("1", "Goalkeeper"),
        ("2", "Defender"),
        ("3", "Midfielder"),
        ("4", "Forward"),
    ]
    test_bench = [("12", "Sub1"), ("13", "Sub2")]
    test_team_info = test_team_name, test_formation, test_starters, test_bench
    test_team_tables = []
    test_schema = {}
    log_messages = []
    result = process_team_tables(
        TEST_BUCKET,
        test_prefix,
        "home",
        test_team_info,
        test_team_tables,
        test_schema,
        log_messages,
    )
    assert result is None


def test_process_team_tables_processes_starters_and_bench(s3_client):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    test_formation = "4-2-3-1"
    test_starters = [
        ("1", "Goalkeeper"),
        ("2", "Defender"),
        ("3", "Midfielder"),
        ("4", "Forward"),
    ]
    test_bench = [("12", "Sub1"), ("13", "Sub2")]
    test_team_info = test_team_name, test_formation, test_starters, test_bench
    test_team_tables = []
    test_schema = {}
    log_messages = []

    process_team_tables(
        TEST_BUCKET,
        test_prefix,
        "home",
        test_team_info,
        test_team_tables,
        test_schema,
        log_messages,
    )

    assert "processed home team starters." in log_messages
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/home/starters.csv"
    )
    expected_starters = "Shirt Number,Player\n"
    for shirt_number, player in test_starters:
        expected_starters += f"{shirt_number},{player}\n"
    assert response["Body"].read().decode("utf-8") == expected_starters

    assert "processed home team bench." in log_messages
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/home/bench.csv"
    )
    expected_bench = "Shirt Number,Player\n"
    for shirt_number, player in test_bench:
        expected_bench += f"{shirt_number},{player}\n"
    assert response["Body"].read().decode("utf-8") == expected_bench


def test_prcoess_team_tables_processes_one_table(s3_client, table_generator):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    team_side = "home"
    test_formation = "4-2-3-1"
    test_starters = [
        ("1", "Goalkeeper"),
        ("2", "Defender"),
        ("3", "Midfielder"),
        ("4", "Forward"),
    ]
    test_bench = [("12", "Sub1"), ("13", "Sub2")]
    test_team_info = test_team_name, test_formation, test_starters, test_bench

    test_team_tables = table_generator(1)
    test_schema = {"Summary": ["ColA0", "ColB0"]}
    log_messages = []

    process_team_tables(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_info,
        test_team_tables,
        test_schema,
        log_messages,
    )

    expected_table_name = "Summary"
    expected_table = "ColA0,ColB0\n" + "Row1A0,Row1B0\n" + "Row2A0,Row2B0\n"
    assert f"processed {team_side} team {expected_table_name} table." in log_messages
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/{team_side}/{expected_table_name}.csv"
    )
    assert response["Body"].read().decode("utf-8") == expected_table


def test_prcoess_team_tables_processes_multiple_tables(s3_client, table_generator):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    team_side = "home"
    test_formation = "4-2-3-1"
    test_starters = [
        ("1", "Goalkeeper"),
        ("2", "Defender"),
        ("3", "Midfielder"),
        ("4", "Forward"),
    ]
    test_bench = [("12", "Sub1"), ("13", "Sub2")]
    test_team_info = test_team_name, test_formation, test_starters, test_bench

    test_team_tables = table_generator(5)
    test_schema = {
        "Summary": ["ColA0", "ColB0"],
        "Passing": ["ColA1", "ColB1"],
        "Pass Types": ["ColA2", "ColB2"],
        "Defensive Actions": ["ColA3", "ColB3"],
        "Possession": ["ColA4", "ColB4"],
    }
    log_messages = []

    process_team_tables(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_info,
        test_team_tables,
        test_schema,
        log_messages,
    )

    for i in range(5):
        expected_table_name = table_name_dict[i]
        expected_table = (
            f"ColA{i},ColB{i}\n" + f"Row1A{i},Row1B{i}\n" + f"Row2A{i},Row2B{i}\n"
        )
        assert (
            f"processed {team_side} team {expected_table_name} table." in log_messages
        )
        response = s3_client.get_object(
            Bucket=TEST_BUCKET,
            Key=f"{test_prefix}/{team_side}/{expected_table_name}.csv",
        )
        assert response["Body"].read().decode("utf-8") == expected_table


def test_prcoess_team_tables_processes_multiple_tables_ignoring_tables_not_in_schema(
    s3_client, table_generator
):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_team_name = "Test FC"
    team_side = "home"
    test_formation = "4-2-3-1"
    test_starters = [
        ("1", "Goalkeeper"),
        ("2", "Defender"),
        ("3", "Midfielder"),
        ("4", "Forward"),
    ]
    test_bench = [("12", "Sub1"), ("13", "Sub2")]
    test_team_info = test_team_name, test_formation, test_starters, test_bench

    test_team_tables = table_generator(5)
    test_schema = {
        "Summary": ["ColA0", "ColB0"],
        "Passing": ["ColA1", "ColB1"],
        "Pass Types": ["ColA2", "ColB2"],
        "Defensive Actions": ["ColA3", "ColB3"],
    }
    log_messages = []

    process_team_tables(
        TEST_BUCKET,
        test_prefix,
        team_side,
        test_team_info,
        test_team_tables,
        test_schema,
        log_messages,
    )

    for i in range(4):
        expected_table_name = table_name_dict[i]
        expected_table = (
            f"ColA{i},ColB{i}\n" + f"Row1A{i},Row1B{i}\n" + f"Row2A{i},Row2B{i}\n"
        )
        assert (
            f"processed {team_side} team {expected_table_name} table." in log_messages
        )
        response = s3_client.get_object(
            Bucket=TEST_BUCKET,
            Key=f"{test_prefix}/{team_side}/{expected_table_name}.csv",
        )
        assert response["Body"].read().decode("utf-8") == expected_table

    expected_table_name = table_name_dict[4]
    assert (
        f"processed {team_side} team {expected_table_name} table." not in log_messages
    )
    response = s3_client.list_objects_v2(Bucket=TEST_BUCKET)
    keys = [obj["Key"] for obj in response.get("Contents", [])]
    assert f"{test_prefix}/{team_side}/{expected_table_name}.csv" not in keys
