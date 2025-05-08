from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError
import pytest


from src.shared_utils.get_soup import get_soup

PATCH_PATH = "src.get_soup"


def test_soup_instance_is_returned_with_content_from_request_response():
    test_url = "https://justanillusion.com"
    test_resp_status = 200
    test_resp_text = """
    <html>
        <b>Test body</b>
    </html>
    """
    response_mock = Mock()
    response_mock.status_code = test_resp_status
    response_mock.text = test_resp_text
    with patch(f"{PATCH_PATH}.requests") as requests_mock:
        requests_mock.get.return_value = response_mock
        result = get_soup(test_url)
    expected = "<b>Test body</b>"
    assert isinstance(result, BeautifulSoup)
    assert str(result.b) == expected


def test_a_bad_status_code_raises_an_error():
    test_url = "https://nonexistantendpoint.com"
    test_resp_status = 404
    test_resp_text = ""
    response_mock = Mock()
    response_mock.status_code = test_resp_status
    response_mock.text = test_resp_text
    response_mock.raise_for_status.side_effect = HTTPError("404 It ain't here")
    with patch(f"{PATCH_PATH}.requests.get") as requests_mock:
        requests_mock.return_value = response_mock
        with pytest.raises(HTTPError) as err:
            get_soup(test_url)
    assert str(err.value) == "404 It ain't here"
