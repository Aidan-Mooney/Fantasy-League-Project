import re
from typing import Tuple, Set


from src.shared_utils.get_soup import get_soup


def get_fixture_links(league: str, season: int) -> Set[str]:
    url, regex_string = get_url_and_regex(league, season)
    soup = get_soup(url)
    link_condition = re.compile(regex_string)
    urls = set()
    last_added = None
    for link in soup.find_all("a"):
        data = link.get("href")
        if data is None:
            continue
        elif link_condition.search(data) and data != last_added:
            urls.add(data[12:20])
            last_added = data
    return urls


def get_url_and_regex(league: str, season: int) -> Tuple[str, str]:
    url = f"https://fbref.com/en/comps/9/{season - 1}-{season}/schedule/{season - 1}-{season}-{league}-Scores-and-Fixtures"
    regex_string = r"/en/matches/[a-z\d]{8}/[\w\d-]+-" + league
    return url, regex_string
