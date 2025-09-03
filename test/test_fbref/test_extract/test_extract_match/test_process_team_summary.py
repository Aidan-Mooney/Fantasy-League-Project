from pytest import fixture
from unittest.mock import patch


from fbref.extract.extract_match.process_team_summary import process_team_summary


MODULE_PATH = "fbref.extract.extract_match.process_team_summary"


@fixture(scope="function")
def mock_funcs():
    with (
        patch(f"{MODULE_PATH}.extract_summary") as mock_summary,
        patch(f"{MODULE_PATH}.save_table_bytes") as mock_save,
    ):
        yield mock_summary, mock_save


def test_process_team_summary_returns_none(mock_funcs):
    test_bucket = "bucket"
    test_template = "template"
    test_league = "league"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_match_data = "data"
    test_team_side = "home"
    extract_mock, save_mock = mock_funcs

    test_card_bytes = b"card stuff"
    test_sub_bytes = b"sub stuff"

    extract_mock.return_value = (test_card_bytes, test_sub_bytes)

    result = process_team_summary(
        test_bucket,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_match_data,
        test_team_side,
    )
    assert result is None


def test_prcoess_team_summary_envokes_extract_summary_correctly(mock_funcs):
    test_bucket = "bucket"
    test_template = "template"
    test_league = "league"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_match_data = "data"
    test_team_side = "home"

    test_card_bytes = b"card stuff"
    test_sub_bytes = b"sub stuff"

    extract_mock, save_mock = mock_funcs
    extract_mock.return_value = (test_card_bytes, test_sub_bytes)

    process_team_summary(
        test_bucket,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_match_data,
        test_team_side,
    )

    args, _ = extract_mock.call_args
    assert args == (test_match_data, test_team_side)


def test_prcoess_team_summary_saves_card_data(mock_funcs):
    test_bucket = "bucket"
    test_template = "template"
    test_league = "league"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_match_data = "data"
    test_team_side = "home"

    expected_file_name = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}/cards.csv"

    test_card_bytes = b"card stuff"
    test_sub_bytes = b"sub stuff"

    extract_mock, save_mock = mock_funcs
    extract_mock.return_value = (test_card_bytes, test_sub_bytes)

    process_team_summary(
        test_bucket,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_match_data,
        test_team_side,
    )

    args, kwargs = save_mock.call_args_list[0]
    assert args == (test_bucket, expected_file_name, test_card_bytes)
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "cards"


def test_prcoess_team_summary_saves_subs_data(mock_funcs):
    test_bucket = "bucket"
    test_template = "template"
    test_league = "league"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_match_data = "data"
    test_team_side = "home"

    expected_file_name = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}/subs.csv"

    test_card_bytes = b"card stuff"
    test_sub_bytes = b"sub stuff"

    extract_mock, save_mock = mock_funcs
    extract_mock.return_value = (test_card_bytes, test_sub_bytes)

    process_team_summary(
        test_bucket,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_match_data,
        test_team_side,
    )

    args, kwargs = save_mock.call_args_list[1]
    assert args == (test_bucket, expected_file_name, test_sub_bytes)
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "subs"
