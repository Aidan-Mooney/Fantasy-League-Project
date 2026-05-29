from pytest import fixture
from unittest.mock import patch


from fbref.extract.extract_match.process_match_tables import process_match_tables


MODULE_PATH = "fbref.extract.extract_match.process_match_tables"


@fixture(scope="function")
def mock_funcs():
    with (
        patch(f"{MODULE_PATH}.process_lineup_data") as mock_process_lineup_data,
        patch(f"{MODULE_PATH}.process_team_tables") as mock_process_team_table,
        patch(f"{MODULE_PATH}.save_table_bytes") as mock_save_table_bytes,
    ):
        yield mock_process_lineup_data, mock_process_team_table, mock_save_table_bytes


def test_process_match_tables_returns_nothing(mock_funcs, extract_bucket_name):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_raw_tables = [i for i in range(20)]
    test_table_schema = {"test": ["A", "B"]}

    result = process_match_tables(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_raw_tables,
        test_table_schema,
    )

    assert result is None


def test_process_match_tables_envokes_lineup_data_twice_with_home_and_away_lineups(
    mock_funcs, extract_bucket_name
):
    ""
