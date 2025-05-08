import pytest
from unittest.mock import patch, Mock


@pytest.fixture
def mock_requests_get():
    with patch("src.shared_utils.get_soup.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><b><h1>Default Page</h1></b></html>"

        mock_get.return_value = mock_response
        yield mock_get, mock_response
