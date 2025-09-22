from bs4 import Tag


def extract_match_row(row: Tag) -> str:
    if "spacer" in row.get("class", []):
        return ""

    cells = row.find_all(["th", "td"])
    data = {cell["data-stat"]: cell for cell in cells if cell.has_attr("data-stat")}

    gameweek = data["gameweek"].get_text(strip=True)
    date = data["date"].get_text(strip=True)
    home = data["home_team"].get_text(strip=True)
    away = data["away_team"].get_text(strip=True)

    score_cell = data.get("score").find("a")
    fixture_id = score_cell["href"][12:20] if score_cell else None
    return f"{home},{away},{gameweek},{date},{fixture_id}\n"
