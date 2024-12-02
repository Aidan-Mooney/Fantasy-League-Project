from unittest.mock import patch

from src.extract import extract

PATCH_PATH = "src.extract"


def test_extract_calls_the_two_different_extract_functions():
    test_season = 2024
    with patch(f"{PATCH_PATH}.extract_fbref") as fbref_mock:
        with patch(f"{PATCH_PATH}.extract_fpl") as fpl_mock:
            extract(test_season)
    assert fbref_mock.call_count == 1
    assert fpl_mock.call_count == 1
    fbref_mock.assert_called_with(test_season)
    fpl_mock.assert_called_with(test_season)
