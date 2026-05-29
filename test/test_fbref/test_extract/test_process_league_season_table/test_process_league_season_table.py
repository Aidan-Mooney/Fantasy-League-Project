from fbref.extract.process_league_season_table.process_league_season_table import (
    process_league_season_table,
)


def test_process_league_season_table_returns_a_list(mock_requests_get):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <table>
        <tbody>
            <tr>
            <th data-stat="gameweek">1</th>
            <td data-stat="date">2025-08-15</td>
            <td data-stat="home_team"><a>Liverpool</a></td>
            <td data-stat="score"><a href="/en/matches/a071faa8/Liverpool-Bournemouth">4-2</a></td>
            <td data-stat="away_team"><a>Bournemouth</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">2</th>
            <td data-stat="date">2025-09-01</td>
            <td data-stat="home_team"><a>Fulham</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Brentford</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">3</th>
            <td data-stat="date">2025-08-22</td>
            <td data-stat="home_team"><a>Chelsea</a></td>
            <td data-stat="score"><a href="/en/matches/b1234567/Chelsea-Arsenal">2-1</a></td>
            <td data-stat="away_team"><a>Arsenal</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">4</th>
            <td data-stat="date">2025-09-08</td>
            <td data-stat="home_team"><a>Everton</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Spurs</a></td>
            </tr>
        </tbody>
        </table>
        """
    test_template = "test"
    test_league = "Premier-League"
    test_season = 2025
    result = process_league_season_table(test_template, test_league, test_season)
    assert isinstance(result, list)
    for id in result:
        assert isinstance(id, str)


def test_process_league_season_table_returns_no_fixture_codes_but_saves_full_table_of_unplayed_matches(
    mock_requests_get,
):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <table>
        <tbody>
            <tr>
            <th data-stat="gameweek">1</th>
            <td data-stat="date">2025-09-01</td>
            <td data-stat="home_team"><a>Fulham</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Brentford</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">2</th>
            <td data-stat="date">2025-09-08</td>
            <td data-stat="home_team"><a>Everton</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Spurs</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">3</th>
            <td data-stat="date">2025-09-15</td>
            <td data-stat="home_team"><a>West Ham</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Leeds</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">4</th>
            <td data-stat="date">2025-09-22</td>
            <td data-stat="home_team"><a>Brighton</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Leicester</a></td>
            </tr>
        </tbody>
        </table>
        """
    test_template = "test"
    test_league = "Premier-League"
    test_season = 2025
    result = process_league_season_table(test_template, test_league, test_season)
    assert len(result) == 0


def test_process_league_season_returns_full_list_of_codes_and_saves_full_table_of_played_matches(
    mock_requests_get,
):
    _, mock_response = mock_requests_get
    id_list = ["a071faa8", "b1234567", "c7654321", "d9876543"]
    mock_response.text = """
        <table>
        <tbody>
            <tr>
            <th data-stat="gameweek">1</th>
            <td data-stat="date">2025-08-15</td>
            <td data-stat="home_team"><a>Liverpool</a></td>
            <td data-stat="score"><a href="/en/matches/{0}/Liverpool-Bournemouth">4-2</a></td>
            <td data-stat="away_team"><a>Bournemouth</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">2</th>
            <td data-stat="date">2025-08-22</td>
            <td data-stat="home_team"><a>Chelsea</a></td>
            <td data-stat="score"><a href="/en/matches/{1}/Chelsea-Arsenal">2-1</a></td>
            <td data-stat="away_team"><a>Arsenal</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">3</th>
            <td data-stat="date">2025-08-29</td>
            <td data-stat="home_team"><a>Man City</a></td>
            <td data-stat="score"><a href="/en/matches/{2}/ManCity-United">3-0</a></td>
            <td data-stat="away_team"><a>Man United</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">4</th>
            <td data-stat="date">2025-09-05</td>
            <td data-stat="home_team"><a>Spurs</a></td>
            <td data-stat="score"><a href="/en/matches/{3}/Spurs-Everton">1-1</a></td>
            <td data-stat="away_team"><a>Everton</a></td>
            </tr>
        </tbody>
        </table>
        """.format(*id_list)
    test_template = "test"
    test_league = "Premier-League"
    test_season = 2025
    result = process_league_season_table(test_template, test_league, test_season)
    assert result == id_list


def test_process_league_season_returns_some_codes_and_saves_full_table_of_played_and_unplayed_matches(
    mock_requests_get,
):
    _, mock_response = mock_requests_get
    id_list = ["a071faa8", "b1234567"]
    mock_response.text = """
        <table>
        <tbody>
            <tr>
            <th data-stat="gameweek">1</th>
            <td data-stat="date">2025-08-15</td>
            <td data-stat="home_team"><a>Liverpool</a></td>
            <td data-stat="score"><a href="/en/matches/{0}/Liverpool-Bournemouth">4-2</a></td>
            <td data-stat="away_team"><a>Bournemouth</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">2</th>
            <td data-stat="date">2025-09-01</td>
            <td data-stat="home_team"><a>Fulham</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Brentford</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">3</th>
            <td data-stat="date">2025-08-22</td>
            <td data-stat="home_team"><a>Chelsea</a></td>
            <td data-stat="score"><a href="/en/matches/{1}/Chelsea-Arsenal">2-1</a></td>
            <td data-stat="away_team"><a>Arsenal</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">4</th>
            <td data-stat="date">2025-09-08</td>
            <td data-stat="home_team"><a>Everton</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Spurs</a></td>
            </tr>
        </tbody>
        </table>
        """.format(*id_list)
    test_template = "test"
    test_league = "Premier-League"
    test_season = 2025
    result = process_league_season_table(test_template, test_league, test_season)
    assert result == id_list


def test_process_league_season_ignores_spacers(
    mock_requests_get,
):
    _, mock_response = mock_requests_get
    id_list = ["a071faa8", "b1234567"]
    mock_response.text = """
        <table>
        <tbody>
            <tr>
            <th data-stat="gameweek">1</th>
            <td data-stat="date">2025-08-15</td>
            <td data-stat="home_team"><a>Liverpool</a></td>
            <td data-stat="score"><a href="/en/matches/{0}/Liverpool-Bournemouth">4-2</a></td>
            <td data-stat="away_team"><a>Bournemouth</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">2</th>
            <td data-stat="date">2025-09-01</td>
            <td data-stat="home_team"><a>Fulham</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Brentford</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">3</th>
            <td data-stat="date">2025-08-22</td>
            <td data-stat="home_team"><a>Chelsea</a></td>
            <td data-stat="score"><a href="/en/matches/{1}/Chelsea-Arsenal">2-1</a></td>
            <td data-stat="away_team"><a>Arsenal</a></td>
            </tr>
            <tr>
            <th data-stat="gameweek">4</th>
            <td data-stat="date">2025-09-08</td>
            <td data-stat="home_team"><a>Everton</a></td>
            <td data-stat="score"></td>
            <td data-stat="away_team"><a>Spurs</a></td>
            </tr>
        </tbody>
        </table>
        """.format(*id_list)
    test_template = "test"
    test_league = "Premier-League"
    test_season = 2025
    result = process_league_season_table(test_template, test_league, test_season)
    assert result == id_list
