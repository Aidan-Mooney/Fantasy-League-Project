from bs4 import BeautifulSoup
from pytest import fixture


from fbref.extract.extract_match.configure_players_bytes import configure_players_bytes


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


def test_configure_players_bytes_returns_a_list_of_tuples_of_two_strings(
    soup_rows_helper,
):
    players = [
        ("1", "Goalkeeper Smith"),
        ("2", "Defender Jones"),
        ("3", "Defender Pat"),
    ]
    input_vals = soup_rows_helper(players)
    result = configure_players_bytes(input_vals)
    assert isinstance(result, bytes)


def test_configure_players_bytes_returns_one_player_correctly(soup_rows_helper):
    players = [("1", "Goalkeeper Smith")]
    input_vals = soup_rows_helper(players)
    result = configure_players_bytes(input_vals)
    expected = "Shirt Number,Player\n" + "1,Goalkeeper Smith\n"
    assert result.decode() == expected


def test_configure_players_bytes_returns_multiple_players_correctly(soup_rows_helper):
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
    result = configure_players_bytes(input_vals)
    expected = (
        "Shirt Number,Player\n"
        + "1,Goalkeeper Smith\n"
        + "2,Defender Jones\n"
        + "3,Defender Pat\n"
        + "4,Defender Gordon\n"
        + "5,Defender McNulty\n"
        + "6,Midfielder Bruno\n"
        + "7,Midfielder Joey\n"
        + "8,Midfielder Burn\n"
        + "9,Midfielder Kyle\n"
        + "10,Forward Mooney\n"
        + "11,Forward Ainsworth\n"
    )
    assert result.decode() == expected


def test_configure_players_bytes_returns_multiple_players_correctly_with_icons(
    soup_rows_helper,
):
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
    result = configure_players_bytes(input_vals)
    expected = (
        "Shirt Number,Player\n"
        + "1,Goalkeeper Smith\n"
        + "2,Defender Jones\n"
        + "3,Defender Pat\n"
        + "4,Defender Gordon\n"
        + "5,Defender McNulty\n"
        + "6,Midfielder Bruno\n"
        + "7,Midfielder Joey\n"
        + "8,Midfielder Burn\n"
        + "9,Midfielder Kyle\n"
        + "10,Forward Mooney\n"
        + "11,Forward Ainsworth\n"
    )
    assert result.decode() == expected
