from bs4 import BeautifulSoup
from pytest import fixture
from unittest.mock import patch


from fbref.extract.extract_match.process_lineup_data import process_lineup_data


MODULE_PATH = "fbref.extract.extract_match.process_lineup_data"


@fixture(scope="function")
def soup_input_helper():
    def _setup(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("table")

    return _setup


@fixture(scope="function")
def mock_save():
    with (
        patch(f"{MODULE_PATH}.save_table_bytes") as mock,
    ):
        yield mock


def test_process_lineup_data_returns_a_string(
    soup_input_helper,
    mock_save,
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_html = """
    <table>
        <tr><th colspan="2">Test FC (4-2-3-1)</th></tr>
        <tr><td>1</td><td>Goalkeeper</td></tr>
        <tr><td>2</td><td>Right Back</td></tr>
        <tr><td>3</td><td>Centre Back</td></tr>
        <tr><td>4</td><td>Left Back</td></tr>
        <tr><td>5</td><td>Midfielder</td></tr>
        <tr><td>6</td><td>Attacking Mid</td></tr>
        <tr><td>7</td><td>Striker</td></tr>
        <tr><td>8</td><td>Winger</td></tr>
        <tr><th colspan="2">Bench</th></tr>
        <tr><td>12</td><td>Sub Keeper</td></tr>
        <tr><td>13</td><td>Sub Defender</td></tr>
        <tr><td>14</td><td>Sub Mid</td></tr>
    </table>
    """
    input_val = soup_input_helper(test_html)
    result = process_lineup_data(
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        input_val,
    )
    assert isinstance(result, str)


def test_process_lineup_data_returns_the_correct_formation(
    soup_input_helper, mock_save
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_html = """
    <table>
        <tr><th colspan="2">Test FC (4-2-3-1)</th></tr>
        <tr><td>1</td><td>Goalkeeper</td></tr>
        <tr><td>2</td><td>Right Back</td></tr>
        <tr><td>3</td><td>Centre Back</td></tr>
        <tr><td>4</td><td>Left Back</td></tr>
        <tr><td>5</td><td>Midfielder</td></tr>
        <tr><td>6</td><td>Attacking Mid</td></tr>
        <tr><td>7</td><td>Striker</td></tr>
        <tr><td>8</td><td>Winger</td></tr>
        <tr><th colspan="2">Bench</th></tr>
        <tr><td>12</td><td>Sub Keeper</td></tr>
        <tr><td>13</td><td>Sub Defender</td></tr>
        <tr><td>14</td><td>Sub Mid</td></tr>
    </table>
    """
    input_val = soup_input_helper(test_html)
    result = process_lineup_data(
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        input_val,
    )
    assert result == "4-2-3-1"


def test_process_lineup_data_saves_the_starters(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_html = """
    <table>
        <tr><th colspan="2">Test FC (4-2-3-1)</th></tr>
        <tr><td>1</td><td>Goalkeeper</td></tr>
        <tr><td>2</td><td>Right Back</td></tr>
        <tr><td>3</td><td>Centre Back</td></tr>
        <tr><td>4</td><td>Left Back</td></tr>
        <tr><td>5</td><td>Midfielder</td></tr>
        <tr><td>6</td><td>Attacking Mid</td></tr>
        <tr><td>7</td><td>Striker</td></tr>
        <tr><td>8</td><td>Winger</td></tr>
        <tr><th colspan="2">Bench</th></tr>
        <tr><td>12</td><td>Sub Keeper</td></tr>
        <tr><td>13</td><td>Sub Defender</td></tr>
        <tr><td>14</td><td>Sub Mid</td></tr>
    </table>
    """
    input_val = soup_input_helper(test_html)
    process_lineup_data(
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        input_val,
    )
    expected_file_name = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}/starters.csv"
    expected_input_bytes = (
        "Shirt Number,Player\n"
        + "1,Goalkeeper\n"
        + "2,Right Back\n"
        + "3,Centre Back\n"
        + "4,Left Back\n"
        + "5,Midfielder\n"
        + "6,Attacking Mid\n"
        + "7,Striker\n"
        + "8,Winger\n"
    ).encode("utf-8")
    args, kwargs = mock_save.call_args_list[0]
    assert args == (extract_bucket_name, expected_file_name, expected_input_bytes)
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "starters"


def test_process_lineup_data_saves_the_bench(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_html = """
    <table>
        <tr><th colspan="2">Test FC (4-2-3-1)</th></tr>
        <tr><td>1</td><td>Goalkeeper</td></tr>
        <tr><td>2</td><td>Right Back</td></tr>
        <tr><td>3</td><td>Centre Back</td></tr>
        <tr><td>4</td><td>Left Back</td></tr>
        <tr><td>5</td><td>Midfielder</td></tr>
        <tr><td>6</td><td>Attacking Mid</td></tr>
        <tr><td>7</td><td>Striker</td></tr>
        <tr><td>8</td><td>Winger</td></tr>
        <tr><th colspan="2">Bench</th></tr>
        <tr><td>12</td><td>Sub Keeper</td></tr>
        <tr><td>13</td><td>Sub Defender</td></tr>
        <tr><td>14</td><td>Sub Mid</td></tr>
    </table>
    """
    input_val = soup_input_helper(test_html)
    process_lineup_data(
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        input_val,
    )
    expected_file_name = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}/bench.csv"
    expected_input_bytes = (
        "Shirt Number,Player\n"
        + "12,Sub Keeper\n"
        + "13,Sub Defender\n"
        + "14,Sub Mid\n"
    ).encode("utf-8")
    args, kwargs = mock_save.call_args_list[1]
    assert args == (extract_bucket_name, expected_file_name, expected_input_bytes)
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "bench"


def test_process_lineup_data_saves_everything_correctly(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_html = """
    <table>
        <tr><th colspan="2">Test FC (4-2-3-1)</th></tr>
        <tr><td>1</td><td>Goalkeeper</td></tr>
        <tr><td>2</td><td>Right Back</td></tr>
        <tr><td>3</td><td>Centre Back</td></tr>
        <tr><td>4</td><td>Left Back</td></tr>
        <tr><td>5</td><td>Midfielder</td></tr>
        <tr><td>6</td><td>Attacking Mid</td></tr>
        <tr><td>7</td><td>Striker</td></tr>
        <tr><td>8</td><td>Winger</td></tr>
        <tr><th colspan="2">Bench</th></tr>
        <tr><td>12</td><td>Sub Keeper</td></tr>
        <tr><td>13</td><td>Sub Defender</td></tr>
        <tr><td>14</td><td>Sub Mid</td></tr>
    </table>
    """
    input_val = soup_input_helper(test_html)
    process_lineup_data(
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        input_val,
    )

    prefix = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}"
    expected_starter_bytes = (
        "Shirt Number,Player\n"
        + "1,Goalkeeper\n"
        + "2,Right Back\n"
        + "3,Centre Back\n"
        + "4,Left Back\n"
        + "5,Midfielder\n"
        + "6,Attacking Mid\n"
        + "7,Striker\n"
        + "8,Winger\n"
    ).encode("utf-8")
    args, kwargs = mock_save.call_args_list[0]
    assert args == (
        extract_bucket_name,
        f"{prefix}/starters.csv",
        expected_starter_bytes,
    )
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "starters"

    expected_bench_bytes = (
        "Shirt Number,Player\n"
        + "12,Sub Keeper\n"
        + "13,Sub Defender\n"
        + "14,Sub Mid\n"
    ).encode("utf-8")
    args, kwargs = mock_save.call_args_list[1]
    assert args == (
        extract_bucket_name,
        f"{prefix}/bench.csv",
        expected_bench_bytes,
    )
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "bench"


def test_process_lineup_data_returns_everything_correctly_with_event_icons(
    soup_input_helper, mock_save, extract_bucket_name
):
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_fixture_id = "a2c4e"
    test_team_side = "home"
    test_html = """
    <table>
        <tr><th colspan="2">Test FC (4-2-3-1)</th></tr>
        <tr><td>1</td><td>Goalkeeper<div class="event_icon yellow_card"></div></td></tr>
        <tr><td>2</td><td>Right Back<div class="event_icon goal"></div></td></tr>
        <tr><td>3</td><td>Centre Back</td></tr>
        <tr><td>4</td><td>Left Back</td></tr>
        <tr><td>5</td><td>Midfielder</td></tr>
        <tr><td>6</td><td>Attacking Mid<div class="event_icon substitute_in"></div></td></tr>
        <tr><td>7</td><td>Striker</td></tr>
        <tr><td>8</td><td>Winger</td></tr>
        <tr><th colspan="2">Bench</th></tr>
        <tr><td>12</td><td>Sub Keeper</td></tr>
        <tr><td>13</td><td>Sub Defender<div class="event_icon yellow_card"></div></td></tr>
        <tr><td>14</td><td>Sub Mid</td></tr>
    </table>
    """
    input_val = soup_input_helper(test_html)
    process_lineup_data(
        test_template,
        test_league,
        test_season,
        test_fixture_id,
        test_team_side,
        input_val,
    )

    prefix = f"{test_template}/{test_league}/{test_season - 1}-{test_season}/{test_fixture_id}/{test_team_side}"
    expected_starter_bytes = (
        "Shirt Number,Player\n"
        + "1,Goalkeeper\n"
        + "2,Right Back\n"
        + "3,Centre Back\n"
        + "4,Left Back\n"
        + "5,Midfielder\n"
        + "6,Attacking Mid\n"
        + "7,Striker\n"
        + "8,Winger\n"
    ).encode("utf-8")
    args, kwargs = mock_save.call_args_list[0]
    assert args == (
        extract_bucket_name,
        f"{prefix}/starters.csv",
        expected_starter_bytes,
    )
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "starters"

    expected_bench_bytes = (
        "Shirt Number,Player\n"
        + "12,Sub Keeper\n"
        + "13,Sub Defender\n"
        + "14,Sub Mid\n"
    ).encode("utf-8")
    args, kwargs = mock_save.call_args_list[1]
    assert args == (
        extract_bucket_name,
        f"{prefix}/bench.csv",
        expected_bench_bytes,
    )
    assert kwargs["template"] == test_template
    assert kwargs["league"] == test_league
    assert kwargs["season"] == test_season
    assert kwargs["fixture_id"] == test_fixture_id
    assert kwargs["team_side"] == test_team_side
    assert kwargs["table_name"] == "bench"
