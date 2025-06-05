from bs4 import BeautifulSoup
from pytest import fixture
from unittest.mock import patch

from extract.extract_fbref.extract_match import process_match_summary


MODULE_PATH = "extract.extract_fbref.extract_match"


@fixture(scope="function")
def mock_process_team_summary():
    with patch(f"{MODULE_PATH}.process_team_summary") as mock_process_team_summary:
        yield mock_process_team_summary


def test_process_match_summary_returns_none(mock_process_team_summary):
    html = """
    <div id="events_wrap">
        <div class="event a">
            6\u2019<br>
            1\u20140<br>
            Player A1<br>
            Assist:
            Player A2<br>
            \u2014\xa0Goal
        </div>
        <div class="event a">
            12\u2019<br>
            1\u20140<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event b">
            15\u2019<br>
            1\u20140<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+1\u2019<br>
            1\u20140<br>
            Player A3<br>
            for Player A4<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+4\u2019<br>
            1\u20140<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            50\u2019<br>
            1\u20140<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event b">
            50\u2019<br>
            1\u20140<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1\u20140<br>
            Player A5<br>
            for Player A6<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            90\u2019<br>
            1\u20140<br>
            Player A7<br>
            for Player A8<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_bucket = "extract-bucket"
    test_prefix = "template/Premier-League/2024-2025/12345678"
    log_messages = []
    result = process_match_summary(test_bucket, test_prefix, soup, log_messages)
    assert result is None


def test_process_match_summary_triggers_process_team_summary_with_home_team_and_away_team(
    mock_process_team_summary,
):
    html = """
    <div id="events_wrap">
        <div class="event a">
            6\u2019<br>
            1\u20140<br>
            Player A1<br>
            Assist:
            Player A2<br>
            \u2014\xa0Goal
        </div>
        <div class="event a">
            12\u2019<br>
            1\u20140<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event b">
            15\u2019<br>
            1\u20140<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+1\u2019<br>
            1\u20140<br>
            Player A3<br>
            for Player A4<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+4\u2019<br>
            1\u20140<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            50\u2019<br>
            1\u20140<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event b">
            50\u2019<br>
            1\u20140<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1\u20140<br>
            Player A5<br>
            for Player A6<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            90\u2019<br>
            1\u20140<br>
            Player A7<br>
            for Player A8<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_bucket = "extract-bucket"
    test_prefix = "template/Premier-League/2024-2025/12345678"
    log_messages = []
    process_match_summary(test_bucket, test_prefix, soup, log_messages)
    expected_summary = soup.find("div", {"id": "events_wrap"})
    assert mock_process_team_summary.call_count == 2

    first_call_args = mock_process_team_summary.call_args_list[0]
    second_call_args = mock_process_team_summary.call_args_list[1]
    args1, kwargs1 = first_call_args
    args2, kwargs2 = second_call_args

    assert args1 == (test_bucket, test_prefix, expected_summary, "home", log_messages)
    assert args2 == (test_bucket, test_prefix, expected_summary, "away", log_messages)
    assert len(kwargs1) == 0
    assert len(kwargs1) == 0
