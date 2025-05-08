import re


from shared_utils.get_soup import get_soup


def get_fixture_links(season: int, league: str):
    url = f"https://fbref.com/en/comps/9/{season - 1}-{season}/schedule/{season - 1}-{season}-{league}-Scores-and-Fixtures"
    soup = get_soup(url)
    link_condition = re.compile(r"/en/matches/[a-z\d]{8}/[\w\d-]+-" + league)
    urls = []
    last_added = None
    for link in soup.find_all("a"):
        data = link.get("href")
        if data is None:
            continue
        elif link_condition.search(data) and data != last_added:
            urls.append(data[12:20])
            last_added = data
    return urls
