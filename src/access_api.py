import requests


def access_api(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
