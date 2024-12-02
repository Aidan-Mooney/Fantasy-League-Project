import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("INSERT HTML ERROR WHEN YOU KNOW HOW TO MOCK THIS")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
