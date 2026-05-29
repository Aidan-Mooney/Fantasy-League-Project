import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    """
    Fetch the HTML content of a webpage and parse it into a BeautifulSoup object.

    Args:
        url: The URL of the webpage to retrieve.

    Returns:
        A BeautifulSoup object containing the parsed HTML of the webpage.

    Raises:
        requests.HTTPError: If the HTTP request fails (e.g., 404, 500).
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
