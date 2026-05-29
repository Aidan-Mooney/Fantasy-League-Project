from bs4 import Tag
from typing import List


def extract_match_row(row: Tag, fixture_ids: List[str]) -> str:
    if "spacer" in row.get("class", []):
        return ""

    cells = row.find_all(["th", "td"])
    data = {cell["data-stat"]: cell for cell in cells if cell.has_attr("data-stat")}

    gameweek = data["gameweek"].get_text(strip=True)
    date = data["date"].get_text(strip=True)
    home = data["home_team"].get_text(strip=True)
    away = data["away_team"].get_text(strip=True)

    new_row_string = f"{home},{away},{gameweek},{date},"

    score_cell = data.get("score").find("a")
    if score_cell:
        fixture_id = score_cell["href"][12:20]
        fixture_ids.append(fixture_id)
        new_row_string += fixture_id
    else:
        new_row_string += "None"

    return new_row_string + "\n"
