from pathlib import Path
from src.extract_fbref import extract_fbref
from src.extract_fpl import extract_fpl


def extract(season):
    Path(f"data/{season}").mkdir(parents=True, exist_ok=True)
    extract_fpl(season)
    extract_fbref(season)
    return
