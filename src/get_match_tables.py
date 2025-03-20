from src.get_soup import get_soup


def get_match_tables(url):
    soup = get_soup(url)
    tables = soup.find_all(lambda tag: tag.name == "table")
    return tables
