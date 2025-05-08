from src.soup_table_to_df import soup_table_to_df


def save_team_tables(path, player_stats_tables, lineup_table, shots_table):
    name_dict = {
        0: "standard",
        1: "passing",
        2: "pass-types",
        3: "def-actions",
        4: "possession",
        5: "misc",
        6: "gk",
    }
    for index, table in enumerate(player_stats_tables):
        soup_table_to_df(table).to_csv(f"{path}/{name_dict[index]}.csv")
    soup_table_to_df(lineup_table).to_csv(f"{path}/lineup.csv")
    soup_table_to_df(shots_table).to_csv(f"{path}/shots.csv")
