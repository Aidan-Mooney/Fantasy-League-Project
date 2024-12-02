from src.extract_fbref import extract_fbref
from src.extract_fpl import extract_fpl


def extract(season):
    extract_fbref(season)
    extract_fpl(season)
    return
