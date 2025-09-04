from pytest import fixture
from unittest.mock import patch
from bs4 import BeautifulSoup


from fbref.extract.extract_match.process_table import process_table


MODULE_PATH = "fbref.extract.extract_match.process_table"


@fixture(scope="function")
def mock_save():
    with (
        patch(f"{MODULE_PATH}.save_table_bytes") as mock,
    ):
        yield mock


@fixture(scope="function")
def soup_input_helper():
    def _setup(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("table")

    return _setup


def test_process_table_returns_none(soup_input_helper, mock_save, extract_bucket_name):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_table_name = "test table"
    input_html = """
    <table>
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
    result = process_table(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_table_name,
        test_table,
        test_schema,
    )
    assert result is None


def test_process_table_does_nothing_if_the_table_name_is_not_in_the_schema(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_table_name = "test table"
    input_html = """
    <table>
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
    process_table(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_table_name,
        test_table,
        test_schema,
    )

    assert mock_save.call_count == 0


def test_process_table_saves_the_table(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_table_name = "test table"
    input_html = """
    <table>
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
    process_table(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_table_name,
        test_table,
        test_schema,
    )
    expected_file_name = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}/{test_table_name}.csv"
    expected_bytes = ("ColA,ColB\n" + "Row1A,Row1B\n" + "Row2A,Row2B\n").encode("utf-8")

    args, kwargs = mock_save.call_args
    assert args == (extract_bucket_name, expected_file_name, expected_bytes)
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == test_table_name


def test_process_table_saves_the_table_with_specific_columns(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_table_name = "test table"
    input_html = """
    <table>
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
    process_table(
        extract_bucket_name,
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        test_table_name,
        test_table,
        test_schema,
    )
    expected_file_name = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}/{test_table_name}.csv"
    expected_bytes = ("ColA\n" + "Row1A\n" + "Row2A\n").encode("utf-8")

    args, kwargs = mock_save.call_args
    assert args == (extract_bucket_name, expected_file_name, expected_bytes)
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == test_table_name
