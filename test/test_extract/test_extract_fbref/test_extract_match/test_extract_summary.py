from bs4 import BeautifulSoup


from extract.extract_fbref.extract_match import extract_summary


def test_extract_summary_returns_a_tuple_of_strings():
    html = """
    <div id="events_wrap">
        <div class="event a">
            20\u2019<br>
            1–0<br>
            Player A1<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)


def test_extract_summary_returns_csvs_with_the_correct_headings():
    html = """
    <div id="events_wrap"></div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    assert result[0] == "time,player,card\n"
    assert result[1] == "time,player OUT,player IN\n"


def test_extract_summary_returns_csvs_with_one_yellow():
    html = """
    <div id="events_wrap">
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A1<br>
            \u2014\xa0Yellow Card
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected = "time,player,card\n" + "45+1,Player A1,Yellow Card\n"
    assert result[0] == expected


def test_extract_summary_returns_csvs_with_multiple_yellows():
    html = """
    <div id="events_wrap">
        <div class="event a">
            10\u2019<br>
            1–0<br>
            Player A1<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            20\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A4<br>
            \u2014\xa0Yellow Card
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected = (
        "time,player,card\n"
        + "10,Player A1,Yellow Card\n"
        + "20,Player A2,Yellow Card\n"
        + "45+1,Player A3,Yellow Card\n"
        + "58,Player A4,Yellow Card\n"
    )
    assert result[0] == expected


def test_extract_summary_returns_csvs_with_multiple_reds():
    html = """
    <div id="events_wrap">
        <div class="event a">
            10\u2019<br>
            1–0<br>
            Player A1<br>
            \u2014\xa0Red Card
        </div>
        <div class="event a">
            20\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Red Card
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Red Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A4<br>
            \u2014\xa0Red Card
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected = (
        "time,player,card\n"
        + "10,Player A1,Red Card\n"
        + "20,Player A2,Red Card\n"
        + "45+1,Player A3,Red Card\n"
        + "58,Player A4,Red Card\n"
    )
    assert result[0] == expected


def test_extract_summary_returns_csvs_with_multiple_second_yellows():
    html = """
    <div id="events_wrap">
        <div class="event a">
            10\u2019<br>
            1–0<br>
            Player A1<br>
            \u2014\xa0Second Yellow Card
        </div>
        <div class="event a">
            20\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Second Yellow Card
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Second Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A4<br>
            \u2014\xa0Second Yellow Card
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected = (
        "time,player,card\n"
        + "10,Player A1,Second Yellow Card\n"
        + "20,Player A2,Second Yellow Card\n"
        + "45+1,Player A3,Second Yellow Card\n"
        + "58,Player A4,Second Yellow Card\n"
    )
    assert result[0] == expected


def test_extract_summary_returns_csvs_with_one_sub():
    html = """
    <div id="events_wrap">
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected = "time,player OUT,player IN\n" + "58,Player A1,Player A2\n"
    assert result[1] == expected


def test_extract_summary_returns_csvs_with_multiple_subs():
    html = """
    <div id="events_wrap">
        <div class="event a">
            12\u2019<br>
            1–0<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            for Player A4<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A5<br>
            for Player A6<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            90\u2019<br>
            1–0<br>
            Player A7<br>
            for Player A8<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected = (
        "time,player OUT,player IN\n"
        + "12,Player A1,Player A2\n"
        + "45+1,Player A3,Player A4\n"
        + "58,Player A5,Player A6\n"
        + "90,Player A7,Player A8\n"
    )
    assert result[1] == expected


def test_extract_summary_ignores_goals():
    html = """
    <div id="events_wrap">
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A1<br>
            Assist:
            Player A2<br>
            \u2014\xa0Goal
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    assert result[0] == "time,player,card\n"
    assert result[1] == "time,player OUT,player IN\n"


def test_extract_summary_can_handle_multiple_of_these_together():
    html = """
    <div id="events_wrap">
        <div class="event a">
            6\u2019<br>
            1–0<br>
            Player A1<br>
            Assist:
            Player A2<br>
            \u2014\xa0Goal
        </div>
        <div class="event a">
            12\u2019<br>
            1–0<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            for Player A4<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+4\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            50\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A5<br>
            for Player A6<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            90\u2019<br>
            1–0<br>
            Player A7<br>
            for Player A8<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "home")
    expected_cards = (
        "time,player,card\n"
        + "45+4,Player A2,Yellow Card\n"
        + "50,Player A3,Yellow Card\n"
    )
    expected_subs = (
        "time,player OUT,player IN\n"
        + "12,Player A1,Player A2\n"
        + "45+1,Player A3,Player A4\n"
        + "58,Player A5,Player A6\n"
        + "90,Player A7,Player A8\n"
    )
    assert result[0] == expected_cards
    assert result[1] == expected_subs


def test_extract_summary_ignores_the_other_side():
    html = """
    <div id="events_wrap">
        <div class="event a">
            6\u2019<br>
            1–0<br>
            Player A1<br>
            Assist:
            Player A2<br>
            \u2014\xa0Goal
        </div>
        <div class="event a">
            12\u2019<br>
            1–0<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            for Player A4<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+4\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            50\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A5<br>
            for Player A6<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            90\u2019<br>
            1–0<br>
            Player A7<br>
            for Player A8<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "away")
    assert result[0] == "time,player,card\n"
    assert result[1] == "time,player OUT,player IN\n"


def test_extract_summary_still_extracts_their_side_whilst_ignoring_the_other():
    html = """
    <div id="events_wrap">
        <div class="event a">
            6\u2019<br>
            1–0<br>
            Player A1<br>
            Assist:
            Player A2<br>
            \u2014\xa0Goal
        </div>
        <div class="event a">
            12\u2019<br>
            1–0<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event b">
            15\u2019<br>
            1–0<br>
            Player A1<br>
            for Player A2<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+1\u2019<br>
            1–0<br>
            Player A3<br>
            for Player A4<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            45+4\u2019<br>
            1–0<br>
            Player A2<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            50\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event b">
            50\u2019<br>
            1–0<br>
            Player A3<br>
            \u2014\xa0Yellow Card
        </div>
        <div class="event a">
            58\u2019<br>
            1–0<br>
            Player A5<br>
            for Player A6<br>
            \u2014\xa0Substitute
        </div>
        <div class="event a">
            90\u2019<br>
            1–0<br>
            Player A7<br>
            for Player A8<br>
            \u2014\xa0Substitute
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    test_match_data = soup.find("div", {"id": "events_wrap"})
    result = extract_summary(test_match_data, "away")
    assert result[0] == "time,player,card\n" + "50,Player A3,Yellow Card\n"
    assert result[1] == "time,player OUT,player IN\n" + "15,Player A1,Player A2\n"
