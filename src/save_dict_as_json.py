import json


def save_dict_as_json(path, dict_data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict_data, f, indent=4)
