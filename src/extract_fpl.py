from src.access_api import access_api
from src.save_dict_as_json import save_dict_as_json
from pathlib import Path


def extract_fpl(season):
    path = f"data/{season}/fpl"
    Path(path).mkdir(parents=True, exist_ok=True)
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    fpl_api = access_api(url)
    for key, data in fpl_api.items():
        save_dict_as_json(f"{path}/{key}.json", {key: data})
    return
