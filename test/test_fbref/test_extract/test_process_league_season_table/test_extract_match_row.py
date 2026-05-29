from bs4 import BeautifulSoup


from fbref.extract.process_league_season_table.extract_match_row import (
    extract_match_row,
)


def test_extract_match_row_returns_a_str():
    html = """<tr>
        <th class="right" data-stat="gameweek" scope="row">1</th>
        <td class="left" data-stat="dayofweek">Fri</td>
        <td class="left" data-stat="date"><a href="/en/matches/2025-08-15">2025-08-15</a></td>
        <td class="right" data-stat="home_team"><a href="/en/squads/822bd0ba/Liverpool-Stats">Liverpool</a></td>
        <td class="center" data-stat="score">
            <a href="/en/matches/a071faa8/Liverpool-Bournemouth-August-15-2025-Premier-League">4–2</a>
        </td>
        <td class="left" data-stat="away_team"><a href="/en/squads/4ba7cbea/Bournemouth-Stats">Bournemouth</a></td>
        </tr>"""

    soup = BeautifulSoup(html, "html.parser")
    test_row = soup.find("tr")
    test_ids = []
    result = extract_match_row(test_row, test_ids)
    assert isinstance(result, str)


def test_extract_match_row_returns_empty_string_from_spacer_and_doesnt_affect_the_id_list():
    html = """<tr class="spacer partial_table result_all" style="background-color:#ddd">
        <th class="right iz" data-stat="gameweek" scope="row"></th>
        <td class="left iz" data-stat="dayofweek"></td>
        <td class="left iz" data-stat="date"></td>
        <td class="right iz" data-stat="home_team"></td>
        <td class="center iz" data-stat="score"></td>
        <td class="left iz" data-stat="away_team"></td>
        </tr>"""

    soup = BeautifulSoup(html, "html.parser")
    test_row = soup.find("tr")
    test_ids = []
    ids_copy = test_ids.copy()
    result = extract_match_row(test_row, test_ids)
    assert result == ""
    assert test_ids == ids_copy


def test_extract_match_row_returns_info_with_no_fixture_id_and_doesnt_affect_the_id_list():
    gameweek = 38
    home_team = "Arsenal"
    away_team = "Newcastle"
    date = "2026-05-13"
    html = f"""<tr>
        <th class="right" data-stat="gameweek" scope="row">{gameweek}</th>
        <td class="left" data-stat="dayofweek">Sat</td>
        <td class="left" data-stat="date"><a href="/en/matches/{date}">{date}</a></td>
        <td class="right" data-stat="home_team"><a href="/en/squads/fd962109/{home_team}-Stats">{home_team}</a></td>
        <td class="center iz" data-stat="score"></td>
        <td class="left" data-stat="away_team"><a href="/en/squads/cd051869/{away_team}-Stats">{away_team}</a></td>
        </tr>"""

    soup = BeautifulSoup(html, "html.parser")
    test_row = soup.find("tr")
    test_ids = []
    ids_copy = test_ids.copy()
    result = extract_match_row(test_row, test_ids)
    expected = f"{home_team},{away_team},{gameweek},{date},None\n"
    assert result == expected
    assert test_ids == ids_copy


def test_extract_match_row_returns_info_with_fixture_id_and_adds_it_to_id_list():
    gameweek = 1
    home_team = "Liverpool"
    away_team = "Bournemouth"
    date = "2025-08-15"
    fixture_id = "a2c4e6g8"
    html = f"""<tr>
        <th class="right" data-stat="gameweek" scope="row">{gameweek}</th>
        <td class="left" data-stat="dayofweek">Sat</td>
        <td class="left" data-stat="date"><a href="/en/matches/{date}">{date}</a></td>
        <td class="right" data-stat="home_team"><a href="/en/squads/fd962109/{home_team}-Stats">{home_team}</a></td>
        <td class="center" data-stat="score">
            <a href="/en/matches/{fixture_id}/{home_team}-{away_team}-August-15-2025-Premier-League">4–2</a>
        </td>
        <td class="left" data-stat="away_team"><a href="/en/squads/cd051869/{away_team}-Stats">{away_team}</a></td>
        </tr>"""

    soup = BeautifulSoup(html, "html.parser")
    test_row = soup.find("tr")
    test_ids = []
    result = extract_match_row(test_row, test_ids)
    expected = f"{home_team},{away_team},{gameweek},{date},{fixture_id}\n"
    assert result == expected
    assert test_ids[-1] == fixture_id
