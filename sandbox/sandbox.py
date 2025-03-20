from pprint import pprint

from src.get_fixture_links import get_fixture_links
from src.get_match_tables import get_match_tables
from src.get_table_data import get_table_data


test_season = 2025
fixtures = get_fixture_links(test_season)
test_fixture = fixtures[0]

test_url = f"https://fbref.com/en/matches/{test_fixture}"

tables = get_match_tables(test_url)
test_table = tables[10]
pprint(get_table_data(test_table))
