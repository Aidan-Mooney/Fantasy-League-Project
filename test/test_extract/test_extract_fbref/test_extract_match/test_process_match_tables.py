from pytest import fixture
from unittest.mock import patch
from bs4 import BeautifulSoup


from extract.extract_fbref.extract_match import process_match_tables


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
def lineup_generator():
    def _setup(team, formation, starters, bench):
        html_string = f"""
            <table>
                <tr><th colspan="2">{team} ({formation})</th></tr>
            """
        for kit_no, player in starters:
            html_string += f"""
                <tr><td>{kit_no}</td><td>{player}</td></tr>
            """
        html_string += """
                <tr><th colspan="2">Bench</th></tr>
            """
        for kit_no, player in bench:
            html_string += f"""
                <tr><td>{kit_no}</td><td>{player}</td></tr>
            """
        html_string += "</table>"
        return html_string

    return _setup


@fixture(scope="function")
def table_generator(lineup_generator):
    def _setup(
        team1, formation1, starters1, bench1, team2, formation2, starters2, bench2
    ):
        html_string = lineup_generator(
            team1, formation1, starters1, bench1
        ) + lineup_generator(team2, formation2, starters2, bench2)
        html_string += """
            <table>
                <thead>
                    <tr><th>IgnoreMe</th></tr>
                </thead>
                <tbody>
                    <tr><td>ok</td></tr>
                </tbody>
            </table>
            """
        for i in range(7):
            html_string += f"""
            <table>
                <caption>{team1} table name {i}</caption>
                <thead>
                    <tr><th>ColA{i}</th><th>ColB{i}</th></tr>
                </thead>
                <tbody>
                    <tr><td>Row1A{i}</td><td>Row1B{i}</td></tr>
                    <tr><td>Row2A{i}</td><td>Row2B{i}</td></tr>
                </tbody>
            </table>
            """
        for i in range(7):
            html_string += f"""
            <table>
                <caption>{team2} table name {i}</caption>
                <thead>
                    <tr><th>ColA{i}</th><th>ColB{i}</th></tr>
                </thead>
                <tbody>
                    <tr><td>Row1A{i}</td><td>Row1B{i}</td></tr>
                    <tr><td>Row2A{i}</td><td>Row2B{i}</td></tr>
                </tbody>
            </table>
            """
        html_string += """
        <table>
            <thead>
                <tr><th>IgnoreMe</th></tr>
            </thead>
            <tbody>
                <tr><td>ok</td></tr>
            </tbody>
        </table>
        """
        for team in [team1, team2]:
            html_string += f"""
            <table>
                <caption>{team} table name {7}</caption>
                <thead>
                    <tr><th>ColA{7}</th><th>ColB{7}</th></tr>
                </thead>
                <tbody>
                    <tr><td>Row1A{7}</td><td>Row1B{7}</td></tr>
                    <tr><td>Row2A{7}</td><td>Row2B{7}</td></tr>
                </tbody>
            </table>
            """
        soup = BeautifulSoup(html_string, "html.parser")
        return soup.find_all("table")

    return _setup


@fixture(scope="function")
def mock_process_team():
    with patch(f"{MODULE_PATH}.process_team_tables") as mock_process_team_table:
        yield mock_process_team_table


def test_process_match_tables_returns_nothing(mock_process_team, table_generator):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_home_team = "Test FC"
    test_home_formation = "4-3-3"
    test_home_starters = [
        ("1", "Goalkeeper"),
        ("4", "Defender"),
        ("8", "Midfielder"),
        ("11", "Forward"),
    ]
    test_home_bench = [
        ("12", "Goalkeeper"),
        ("13", "Defender"),
    ]
    test_away_team = "Develope Club"
    test_away_formation = "4-2-3-1"
    test_away_starters = [
        ("1", "Goalkeeper"),
        ("4", "Defender"),
        ("8", "Midfielder"),
        ("11", "Forward"),
    ]
    test_away_bench = [
        ("12", "Goalkeeper"),
        ("13", "Defender"),
    ]
    test_tables = table_generator(
        test_home_team,
        test_home_formation,
        test_home_starters,
        test_home_bench,
        test_away_team,
        test_away_formation,
        test_away_starters,
        test_away_bench,
    )
    test_schema = {}
    for i in range(8):
        test_schema[f"table name {i}"] = [f"ColA{i}", f"ColB{i}"]
    log_messages = []
    result = process_match_tables(
        TEST_BUCKET, test_prefix, test_tables, test_schema, log_messages
    )
    assert result is None


def test_process_match_tables_processes_teams_and_formation_and_logs_message(
    s3_client, mock_process_team, table_generator
):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_home_team = "Test FC"
    test_home_formation = "4-3-3"
    test_home_starters = [
        ("1", "Goalkeeper"),
        ("4", "Defender"),
        ("8", "Midfielder"),
        ("11", "Forward"),
    ]
    test_home_bench = [
        ("12", "Goalkeeper"),
        ("13", "Defender"),
    ]
    test_away_team = "Develope Club"
    test_away_formation = "4-2-3-1"
    test_away_starters = [
        ("1", "Goalkeeper"),
        ("4", "Defender"),
        ("8", "Midfielder"),
        ("11", "Forward"),
    ]
    test_away_bench = [
        ("12", "Goalkeeper"),
        ("13", "Defender"),
    ]
    test_tables = table_generator(
        test_home_team,
        test_home_formation,
        test_home_starters,
        test_home_bench,
        test_away_team,
        test_away_formation,
        test_away_starters,
        test_away_bench,
    )
    test_schema = {}
    for i in range(8):
        test_schema[f"table name {i}"] = [f"ColA{i}", f"ColB{i}"]
    log_messages = []
    process_match_tables(
        TEST_BUCKET, test_prefix, test_tables, test_schema, log_messages
    )

    assert "processed match info." in log_messages
    expected_table = (
        "side,team,formation\n"
        + f"home,{test_home_team},{test_home_formation}\n"
        + f"away,{test_away_team},{test_away_formation}\n"
    )
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/match-info.csv"
    )
    assert response["Body"].read().decode("utf-8") == expected_table


def test_process_match_tables_envokes_process_team_tables_with_home_and_away_team(
    mock_process_team, table_generator
):
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_home_team = "Test FC"
    test_home_formation = "4-3-3"
    test_home_starters = [
        ("1", "Goalkeeper"),
        ("4", "Defender"),
        ("8", "Midfielder"),
        ("11", "Forward"),
    ]
    test_home_bench = [
        ("12", "Goalkeeper"),
        ("13", "Defender"),
    ]
    test_away_team = "Develope Club"
    test_away_formation = "4-2-3-1"
    test_away_starters = [
        ("1", "Goalkeeper"),
        ("4", "Defender"),
        ("8", "Midfielder"),
        ("11", "Forward"),
    ]
    test_away_bench = [
        ("12", "Goalkeeper"),
        ("13", "Defender"),
    ]
    test_tables = table_generator(
        test_home_team,
        test_home_formation,
        test_home_starters,
        test_home_bench,
        test_away_team,
        test_away_formation,
        test_away_starters,
        test_away_bench,
    )
    test_schema = {}
    for i in range(8):
        test_schema[f"table name {i}"] = [f"ColA{i}", f"ColB{i}"]
    log_messages = []
    process_match_tables(
        TEST_BUCKET, test_prefix, test_tables, test_schema, log_messages
    )
    assert mock_process_team.call_count == 2

    first_call_args = mock_process_team.call_args_list[0]
    second_call_args = mock_process_team.call_args_list[1]
    args1, kwargs1 = first_call_args
    args2, kwargs2 = second_call_args

    assert args1[0] == TEST_BUCKET
    assert args1[1] == test_prefix
    assert args1[2] == "home"
    assert args1[3] == (
        test_home_team,
        test_home_formation,
        test_home_starters,
        test_home_bench,
    )
    assert len(args1[4]) == 8
    assert args1[5] == test_schema
    assert args1[6] == log_messages

    assert args2[0] == TEST_BUCKET
    assert args2[1] == test_prefix
    assert args2[2] == "away"
    assert args2[3] == (
        test_away_team,
        test_away_formation,
        test_away_starters,
        test_away_bench,
    )
    assert len(args2[4]) == 8
    assert args2[5] == test_schema
    assert args2[6] == log_messages

    assert len(kwargs1) == 0
    assert len(kwargs2) == 0
