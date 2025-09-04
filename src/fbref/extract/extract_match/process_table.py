from fbref.extract.save_table_bytes import save_table_bytes
from fbref.extract.extract_match.html_table_to_csv_bytes import html_table_to_csv_bytes


def process_table(
    bucket,
    template,
    league,
    season,
    fixture_id,
    team_side,
    table_name,
    table,
    table_schema,
):
    headings = table_schema.get(table_name, None)
    if headings is not None:
        table_bytes = html_table_to_csv_bytes(table, headings)
        save_table_bytes(
            bucket,
            f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/{table_name}.csv",
            table_bytes,
            template=template,
            league=league,
            season=season,
            fixture_id=fixture_id,
            team_side=team_side,
            table_name=table_name,
        )
