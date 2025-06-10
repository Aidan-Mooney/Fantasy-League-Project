from bs4 import BeautifulSoup
from pytest import fixture


from extract.extract_fbref.extract_match import process_lineup_data


@fixture(scope="function")
def soup_input_helper():
    def _setup(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("table")

    return _setup


def test_process_lineup_data_returns_a_tuple_with_correct_contents(soup_input_helper):
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
    result = process_lineup_data(input_val)
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)
    assert isinstance(result[2], list)
    assert isinstance(result[3], list)


def test_process_lineup_data_returns_the_correct_team_name(soup_input_helper):
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
    result = process_lineup_data(input_val)
    assert result[0] == "Test FC"


def test_process_lineup_data_returns_the_correct_formation(soup_input_helper):
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
    result = process_lineup_data(input_val)
    assert result[1] == "4-2-3-1"


def test_process_lineup_data_returns_the_starters(soup_input_helper):
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
    result = process_lineup_data(input_val)
    expected = [
        ("1", "Goalkeeper"),
        ("2", "Right Back"),
        ("3", "Centre Back"),
        ("4", "Left Back"),
        ("5", "Midfielder"),
        ("6", "Attacking Mid"),
        ("7", "Striker"),
        ("8", "Winger"),
    ]
    assert result[2] == expected


def test_process_lineup_data_returns_the_bench(soup_input_helper):
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
    result = process_lineup_data(input_val)
    expected = [("12", "Sub Keeper"), ("13", "Sub Defender"), ("14", "Sub Mid")]
    assert result[3] == expected


def test_process_lineup_data_returns_everything_correctly(soup_input_helper):
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
    result = process_lineup_data(input_val)
    expected_starters = [
        ("1", "Goalkeeper"),
        ("2", "Right Back"),
        ("3", "Centre Back"),
        ("4", "Left Back"),
        ("5", "Midfielder"),
        ("6", "Attacking Mid"),
        ("7", "Striker"),
        ("8", "Winger"),
    ]
    expected_bench = [("12", "Sub Keeper"), ("13", "Sub Defender"), ("14", "Sub Mid")]
    assert result[0] == "Test FC"
    assert result[1] == "4-2-3-1"
    assert result[2] == expected_starters
    assert result[3] == expected_bench


def test_process_lineup_data_returns_everything_correctly_with_event_icons(
    soup_input_helper,
):
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
    result = process_lineup_data(input_val)
    expected_starters = [
        ("1", "Goalkeeper"),
        ("2", "Right Back"),
        ("3", "Centre Back"),
        ("4", "Left Back"),
        ("5", "Midfielder"),
        ("6", "Attacking Mid"),
        ("7", "Striker"),
        ("8", "Winger"),
    ]
    expected_bench = [("12", "Sub Keeper"), ("13", "Sub Defender"), ("14", "Sub Mid")]
    assert result[0] == "Test FC"
    assert result[1] == "4-2-3-1"
    assert result[2] == expected_starters
    assert result[3] == expected_bench
