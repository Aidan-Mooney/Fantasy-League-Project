from pprint import pprint

from src.extract import extract
from extract_fixtures.get_fixture_links import get_fixture_links


test_season = 2025
# extract(test_season)
x = get_fixture_links(test_season)
print(x)
