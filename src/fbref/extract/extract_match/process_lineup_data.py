import re
from fbref.extract.extract_match.html_helper import html_helper
from fbref.extract.save_table_bytes import save_table_bytes


def process_lineup_data(bucket, template, league, season, fixture_id, team_side, table):
    rows = table.find_all("tr")

    first_header = rows[0].find("th").get_text(strip=True)
    name_formation_condition = re.compile(r"^(.*?)\s*\(([\d\-]+)\)")
    name_formation_match = name_formation_condition.match(first_header)
    formation = name_formation_match.group(2).strip()

    second_header_index = None
    for i, row in enumerate(rows[1:], 1):
        th = row.find("th")
        if th and th.has_attr("colspan"):
            second_header_index = i
            break

    starters_bytes = html_helper(rows[1:second_header_index])
    bench_bytes = html_helper(rows[second_header_index + 1 :])
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/starters.csv",
        starters_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="starters",
    )
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/bench.csv",
        bench_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="bench",
    )
    return formation
