from bs4 import BeautifulSoup
from pytest import fixture
from unittest.mock import patch


from extract.extract_fbref.extract_match import process_team_summary


MODULE_PATH = "extract.extract_fbref.extract_match"
TEST_BUCKET = "extract-bucket"


@fixture(autouse=True)
def patch_s3_client(s3_client):
    with patch(f"{MODULE_PATH}.s3_client", s3_client):
        yield


@fixture(autouse=True)
def create_bucket(s3_client):
    s3_client.create_bucket(
        Bucket=TEST_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


def test_process_team_summary_returns_none():
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
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_match_data = soup.find("div", {"id": "events_wrap"})
    log_message = []
    result = process_team_summary(
        TEST_BUCKET, test_prefix, test_match_data, "home", log_message
    )
    assert result is None


def test_prcoess_team_summary_logs_message_and_posts_card_data_to_bucket(s3_client):
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
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_match_data = soup.find("div", {"id": "events_wrap"})
    log_messages = []
    process_team_summary(
        TEST_BUCKET, test_prefix, test_match_data, "home", log_messages
    )

    assert "processed home team card table." in log_messages
    expected_cards = (
        "time,player,card\n"
        + "45+4,Player A2,Yellow Card\n"
        + "50,Player A3,Yellow Card\n"
    )
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/home/card.csv"
    )
    assert response["Body"].read().decode("utf-8") == expected_cards


def test_prcoess_team_summary_logs_message_and_posts_sub_data_to_bucket(s3_client):
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
    test_prefix = "template/Premier-League/2024-2025/12345678"
    test_match_data = soup.find("div", {"id": "events_wrap"})
    log_messages = []
    process_team_summary(
        TEST_BUCKET, test_prefix, test_match_data, "home", log_messages
    )

    assert "processed home team card table." in log_messages
    expected_subs = (
        "time,player OUT,player IN\n"
        + "12,Player A1,Player A2\n"
        + "45+1,Player A3,Player A4\n"
        + "58,Player A5,Player A6\n"
        + "90,Player A7,Player A8\n"
    )
    response = s3_client.get_object(
        Bucket=TEST_BUCKET, Key=f"{test_prefix}/home/sub.csv"
    )
    assert response["Body"].read().decode("utf-8") == expected_subs
