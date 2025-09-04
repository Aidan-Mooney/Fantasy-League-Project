from io import BytesIO
from fbref.extract.save_table_bytes import save_table_bytes
from fbref.extract.extract_match.process_lineup_data import process_lineup_data
from fbref.extract.extract_match.process_team_tables import process_team_tables


def process_match_tables(
    bucket, template, league, season, fixture_id, raw_html_tables, table_schema
):
    home_formation = process_lineup_data(
        bucket, template, league, season, fixture_id, "home", raw_html_tables[0]
    )
    home_tables = raw_html_tables[3:10] + [raw_html_tables[18]]
    process_team_tables(
        bucket,
        template,
        league,
        season,
        fixture_id,
        "home",
        home_tables,
        table_schema,
    )

    away_formation = process_lineup_data(
        bucket, template, league, season, fixture_id, "away", raw_html_tables[1]
    )
    away_tables = raw_html_tables[10:17] + [raw_html_tables[19]]
    process_team_tables(
        bucket,
        template,
        league,
        season,
        fixture_id,
        "away",
        away_tables,
        table_schema,
    )

    team_info_bytes = BytesIO()
    team_info_bytes.write("side,formation\n".encode("utf-8"))
    team_info_bytes.write(f"home,{home_formation}\n".encode("utf-8"))
    team_info_bytes.write(f"away,{away_formation}\n".encode("utf-8"))
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/match-info.csv",
        team_info_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        table_name="match-info",
    )
