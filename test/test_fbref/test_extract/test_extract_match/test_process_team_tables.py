from pytest import fixture
from unittest.mock import patch
from bs4 import BeautifulSoup


from fbref.extract.extract_match.process_team_tables import (
    process_team_tables,
    table_name_dict,
)


MODULE_PATH = "fbref.extract.extract_match.process_team_tables"


@fixture(scope="function")
def mock_process_table():
    with (
        patch(f"{MODULE_PATH}.process_table") as mock,
    ):
        yield mock


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


def test_process_team_tables_returns_none(mock_process_table, extract_bucket_name):
    test_template = "test_template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_team_tables = []
    test_schema = {}

    result = process_team_tables(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_team_tables,
        test_schema,
    )
    assert result is None


def test_prcoess_team_tables_processes_one_table(
    table_generator, mock_process_table, extract_bucket_name
):
    test_template = "test_template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_team_tables = table_generator(1)
    test_schema = {"Summary": ["ColA0", "ColB0"]}

    process_team_tables(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_team_tables,
        test_schema,
    )

    assert mock_process_table.call_count == 1
    args, _ = mock_process_table.call_args
    assert args[0] == extract_bucket_name
    assert args[1] == test_template
    assert args[2] == test_league
    assert args[3] == test_season
    assert args[4] == test_fixture_id
    assert args[5] == test_team_side
    assert args[6] == table_name_dict[0]
    assert args[7] == test_team_tables[0]
    assert args[8] == test_schema


def test_prcoess_team_tables_processes_multiple_tables(
    table_generator, mock_process_table, extract_bucket_name
):
    test_template = "test_template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_team_tables = table_generator(5)
    test_schema = {
        "Summary": ["ColA0", "ColB0"],
        "Passing": ["ColA1", "ColB1"],
        "Pass Types": ["ColA2", "ColB2"],
        "Defensive Actions": ["ColA3", "ColB3"],
        "Possession": ["ColA4", "ColB4"],
    }

    process_team_tables(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_team_tables,
        test_schema,
    )

    assert mock_process_table.call_count == 5
    for index, item in enumerate(mock_process_table.call_args_list):
        args, _ = item
        assert args[0] == extract_bucket_name
        assert args[1] == test_template
        assert args[2] == test_league
        assert args[3] == test_season
        assert args[4] == test_fixture_id
        assert args[5] == test_team_side
        assert args[6] == table_name_dict[index]
        assert args[7] == test_team_tables[index]
        assert args[8] == test_schema
