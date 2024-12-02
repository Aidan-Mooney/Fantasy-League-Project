from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
import pytest


from src.get_soup import get_soup

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
    with patch(f"{PATCH_PATH}.requests") as requests_mock:
        requests_mock.get.return_value = response_mock
        with pytest.raises(Exception) as err:
            get_soup(test_url)
    assert str(err.value) == "INSERT HTML ERROR WHEN YOU KNOW HOW TO MOCK THIS"
