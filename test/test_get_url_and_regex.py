from src.extract_fixtures.get_fixture_links import get_url_and_regex


def test_get_url_and_regex_returns_a_tuple_containing_two_strings():
    output = get_url_and_regex(1, "Premier-League")
    assert isinstance(output, tuple)
    assert isinstance(output[0], str)
    assert isinstance(output[1], str)


def test_get_url_and_regex_works_for_prem_and_current_season():
    output_url, output_regex_string = get_url_and_regex(2025, "Premier-League")
    assert (
        output_url
        == "https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-Premier-League-Scores-and-Fixtures"
    )
    assert output_regex_string == r"/en/matches/[a-z\d]{8}/[\w\d-]+-Premier-League"


def test_get_url_and_regex_works_for_other_seasons():
    output_url, output_regex_string = get_url_and_regex(2020, "Premier-League")
    assert (
        output_url
        == "https://fbref.com/en/comps/9/2019-2020/schedule/2019-2020-Premier-League-Scores-and-Fixtures"
    )
    assert output_regex_string == r"/en/matches/[a-z\d]{8}/[\w\d-]+-Premier-League"


def test_get_url_and_regex_works_for_other_leagues():
    output_url, output_regex_string = get_url_and_regex(2025, "La-Liga")
    assert (
        output_url
        == "https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-La-Liga-Scores-and-Fixtures"
    )
    assert output_regex_string == r"/en/matches/[a-z\d]{8}/[\w\d-]+-La-Liga"

    output_url, output_regex_string = get_url_and_regex(2025, "Serie-A")
    assert (
        output_url
        == "https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-Serie-A-Scores-and-Fixtures"
    )
    assert output_regex_string == r"/en/matches/[a-z\d]{8}/[\w\d-]+-Serie-A"

    output_url, output_regex_string = get_url_and_regex(2025, "Bundesliga")
    assert (
        output_url
        == "https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-Bundesliga-Scores-and-Fixtures"
    )
    assert output_regex_string == r"/en/matches/[a-z\d]{8}/[\w\d-]+-Bundesliga"

    output_url, output_regex_string = get_url_and_regex(2025, "Ligue-1")
    assert (
        output_url
        == "https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-Ligue-1-Scores-and-Fixtures"
    )
    assert output_regex_string == r"/en/matches/[a-z\d]{8}/[\w\d-]+-Ligue-1"
