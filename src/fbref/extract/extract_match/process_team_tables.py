from fbref.extract.extract_match.process_table import process_table


table_name_dict = {
    0: "Summary",
    1: "Passing",
    2: "Pass Types",
    3: "Defensive Actions",
    4: "Possession",
    5: "Miscellaneous Stats",
    6: "Goalkeeper",
    7: "Shots",
}


def process_team_tables(
    bucket, template, league, season, fixture_id, team_side, team_tables, table_schema
):
    for index, table in enumerate(team_tables):
        table_name = table_name_dict[index]
        process_table(
            bucket,
            template,
            league,
            season,
            fixture_id,
            team_side,
            table_name,
            table,
            table_schema,
        )
