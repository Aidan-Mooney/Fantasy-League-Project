from bs4 import BeautifulSoup
from pytest import fixture


from extract.extract_fbref.extract_match import html_helper


@fixture(scope="function")
def soup_rows_helper():
    def _setup(player_list, with_icons=False):
        html = ""
        for number, name in player_list:
            icon_html = (
                '<div class="event_icon yellow_card"></div><div class="event_icon goal"></div>'
                if with_icons
                else ""
            )
            html += f"""
            <tr>
                <td>{number}</td>
                <td>{name}{icon_html}</td>
            </tr>
            """
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("tr")

    return _setup


def test_html_helper_returns_a_list_of_tuples_of_two_strings(soup_rows_helper):
    players = [
        ("1", "Goalkeeper Smith"),
        ("2", "Defender Jones"),
        ("3", "Defender Pat"),
    ]
    input_vals = soup_rows_helper(players)
    result = html_helper(input_vals)
    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, tuple)
        assert isinstance(i[0], str)
        assert isinstance(i[1], str)


def test_html_helper_returns_one_player_correctly(soup_rows_helper):
    players = [("1", "Goalkeeper Smith")]
    input_vals = soup_rows_helper(players)
    result = html_helper(input_vals)
    assert result == players


def test_html_helper_returns_multiple_players_correctly(soup_rows_helper):
    players = [
        ("1", "Goalkeeper Smith"),
        ("2", "Defender Jones"),
        ("3", "Defender Pat"),
        ("4", "Defender Gordon"),
        ("5", "Defender McNulty"),
        ("6", "Midfielder Bruno"),
        ("7", "Midfielder Joey"),
        ("8", "Midfielder Burn"),
        ("9", "Midfielder Kyle"),
        ("10", "Forward Mooney"),
        ("11", "Forward Ainsworth"),
    ]
    input_vals = soup_rows_helper(players)
    result = html_helper(input_vals)
    assert result == players


def test_html_helper_returns_multiple_players_correctly_with_icons(soup_rows_helper):
    players = [
        ("1", "Goalkeeper Smith"),
        ("2", "Defender Jones"),
        ("3", "Defender Pat"),
        ("4", "Defender Gordon"),
        ("5", "Defender McNulty"),
        ("6", "Midfielder Bruno"),
        ("7", "Midfielder Joey"),
        ("8", "Midfielder Burn"),
        ("9", "Midfielder Kyle"),
        ("10", "Forward Mooney"),
        ("11", "Forward Ainsworth"),
    ]
    input_vals = soup_rows_helper(players, True)
    result = html_helper(input_vals)
    assert result == players
