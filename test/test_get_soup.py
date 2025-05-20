from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import pytest


from get_soup import get_soup


def test_soup_returns_beautiful_soup_instance(mock_requests_get):
    test_url = "https://icantbelieveitsnotaurl.com"
    result = get_soup(test_url)
    assert isinstance(result, BeautifulSoup)


def test_soup_instance_is_returned_with_content_from_request_response(
    mock_requests_get,
):
    test_url = "https://justanillusion.com"
    result = get_soup(test_url)
    expected = "<b><h1>Default Page</h1></b>"
    assert str(result.b) == expected


def test_a_bad_status_code_raises_an_error(mock_requests_get):
    mock_get, mock_response = mock_requests_get
    test_url = "https://nonexistantendpoint.com"
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError(
        "404 Client Error: Not Found"
    )
    with pytest.raises(HTTPError) as exc_info:
        get_soup(test_url)
    assert "404" in str(exc_info.value)
    mock_get.assert_called_once_with(test_url)
