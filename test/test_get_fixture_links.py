# import pytest
from src.extract_fixtures.get_fixture_links import get_fixture_links


def test_get_fixture_links_returns_list_of_strings(mock_requests_get):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <html>
            <b>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code5678/Team-C-Team-D-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code5678/Team-C-Team-D-January-01-2025-Premier-League"></a>
                <a href="/nomatch/11111111">Not a match</a>
                <a>No href here</a>
            </b>
        </html>
    """
    result = get_fixture_links(2025, "Premier-League")
    assert isinstance(result, list)
    for link in result:
        assert isinstance(link, str)


def test_get_fixture_links_returns_an_empty_list_if_no_match_links_are_found(
    mock_requests_get,
):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <html>
            <b>
                <a>No href here</a>
            </b>
        </html>
    """
    result = get_fixture_links(2025, "Premier-League")
    assert len(result) == 0


def test_get_fixture_links_works_with_one_match_link(mock_requests_get):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <html>
            <b>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
            </b>
        </html>
    """
    result = get_fixture_links(2025, "Premier-League")
    assert result == ["code1234"]


def test_get_fixture_links_works_with_one_match_link_with_duplicate(mock_requests_get):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <html>
            <b>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
            </b>
        </html>
    """
    result = get_fixture_links(2025, "Premier-League")
    assert result == ["code1234"]


def test_get_fixture_links_works_with_multiple_duplicates(mock_requests_get):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <html>
            <b>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code5678/Team-C-Team-D-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code5678/Team-C-Team-D-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code9101/Team-E-Team-F-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code9101/Team-E-Team-F-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1121/Team-G-Team-H-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1121/Team-G-Team-H-January-01-2025-Premier-League"></a>
            </b>
        </html>
    """
    result = get_fixture_links(2025, "Premier-League")
    assert result == ["code1234", "code5678", "code9101", "code1121"]


def test_get_fixture_links_ignores_none_match_links(mock_requests_get):
    _, mock_response = mock_requests_get
    mock_response.text = """
        <html>
            <b>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1234/Team-A-Team-B-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code5678/Team-C-Team-D-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code5678/Team-C-Team-D-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code9101/Team-E-Team-F-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code9101/Team-E-Team-F-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1121/Team-G-Team-H-January-01-2025-Premier-League"></a>
                <a href="/en/matches/code1121/Team-G-Team-H-January-01-2025-Premier-League"></a>
                <a href="/nomatch/11111111">Not a match</a>
            </b>
        </html>
    """
    result = get_fixture_links(2025, "Premier-League")
    assert result == ["code1234", "code5678", "code9101", "code1121"]
