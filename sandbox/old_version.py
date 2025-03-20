import pandas as pd
from datetime import datetime, date
import time
import math
from bs4 import BeautifulSoup
import requests
import os
from scipy.stats import binom


class TooManyRequestsError(Exception):
    pass


class TeamNameError(Exception):
    pass


class PositionError(Exception):
    pass


month_dict = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


team_dict = {
    "Brighton": "Brighton and Hove Albion",
    "Manchester Utd": "Manchester United",
    "Newcastle Utd": "Newcastle United",
    "Nott'ham Forest": "Nottingham Forest",
    "Sheffield Utd": "Sheffield United",
    "Tottenham": "Tottenham Hotspur",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhampton Wanderers",
}


def delay_func_prefix(wait_time):
    def delay_func(func):
        def wrapper_func(*args, **kwargs):
            start_time = time.time()
            x = func(*args, **kwargs)
            sleep_time = wait_time + start_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            return x

        return wrapper_func

    return delay_func


def user_input_options(options, question, add_none=False, index_counter=None):
    if index_counter:
        print("This is item {0} out of {1}.".format(index_counter[0], index_counter[1]))
    print(question)
    for index, item in enumerate(options):
        print("{0}. {1}".format(index + 1, item))
    if add_none:
        print(str(len(options) + 1) + ". None")
    print("Please return the number associated with the correct item.")
    try:
        correct_index = int(input(""))
        if add_none and correct_index == len(options) + 1 or correct_index is None:
            return None
        return options[correct_index - 1]
    except ValueError:
        print("Please input a number.")
        return user_input_options(options, question, add_none)
    except IndexError:
        print("Please input a number in the correct range.")
        return user_input_options(options, question, add_none)
    except Exception as e:
        raise e


def slice_list(sorted_list, min_k, max_k):
    first_cut = find_min_max_and_slice(sorted_list, min_k, operator_greater_equal)
    second_cut = find_min_max_and_slice(first_cut[::-1], max_k, operator_less_equal)
    return second_cut[::-1]


def find_min_max_and_slice(sorted_list, k, operator):
    for index, num in enumerate(sorted_list):
        if operator(num, k):
            return sorted_list[index:]
    return []


def operator_less_equal(a, b):
    return a <= b


def operator_greater_equal(a, b):
    return a >= b


def similar_elements(a, b):
    return list(set(a) & set(b))


def does_file_existence(path, file_name):
    file_list = os.listdir(path)
    return file_name in file_list


def get_permission(url):
    reqs = requests.get(url)
    if reqs.status_code == 429:
        raise TooManyRequestsError(datetime.now().strftime("%H:%M:%S"))
    return reqs


@delay_func_prefix(wait_time=5)
def get_df_list_from_url(url):
    df_list = pd.read_html(url)
    return df_list


@delay_func_prefix(wait_time=5)
def get_soup_from_url(url):
    reqs = get_permission(url)
    soup = BeautifulSoup(reqs.text, "lxml")
    return soup


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def get_team_list(url):
    df = get_df_list_from_url(url)[0]
    team_list = df["Squad"].to_list()
    return [team_dict.get(name, name) for name in team_list]


def find_team_names(team_list, options):
    for index, name in enumerate(options):
        if name == "Derby":
            options = options[index + 1 :]
            break
    for i in range(1, len(options)):
        team_option = " ".join(options[:i])
        if team_option in team_list:
            return team_option, " ".join(options[i:])
    raise TeamNameError(f"Options doesn't contain a valid name: {options}")


def get_gameweeks(url):
    date_dict = get_fixture_links(url)

    df = get_df_list_from_url(url)[0]
    gameweek = 1
    gameweek_dict = {}
    done_date_list = []
    for index, row in df.iterrows():
        if math.isnan(row["Wk"]):
            continue
        elif row["Wk"] == gameweek + 1:
            gameweek += 1
        date_list = row["Date"].split("-")
        date_item = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        if date_item in done_date_list:
            continue
        gameweek_dict.setdefault(gameweek, [])
        gameweek_dict[gameweek] += date_dict[date_item]
        done_date_list.append(date_item)
    return gameweek_dict


def get_fixture_links(url):
    soup = get_soup_from_url(url)

    urls_list = []
    for link in soup.find_all("a"):
        data = link.get("href")
        if data is None:
            continue
        elif "matches" in data and len(data) > 25:
            if data not in urls_list:
                urls_list.append(data)
    return urls_list


def format_columns(df_heading):
    if df_heading[:9] == "Unnamed: ":
        if int(df_heading[9]) < 6:
            return "Player_Info"
        else:
            return "Other"
    return df_heading


def get_headings(df, index_list):
    return [list(df)[i] for i in index_list]


def format_df(df, headings=None):
    df.columns = ["{0}-{1}".format(format_columns(x[0]), x[1]) for x in list(df)]
    if headings:
        df.drop(columns=get_headings(df, headings), inplace=True)
    return df


def create_main_df(df_list):
    drop_index_dict = {
        0: [8, 13, 16, 19],
        2: [13],
        3: [15, 17],
        4: [12, 13, 14, 21],
        5: [7, 11, 14, 17, 21],
    }

    df_base = format_df(
        df_list[0], [x for x in range(12, 18)] + [y for y in range(21, 31)]
    )
    del df_list[0]
    for index, df in enumerate(df_list):
        df = format_df(df, drop_index_dict.get(index))
        headings = similar_elements(list(df), list(df_base))
        df_base = pd.merge(df_base, df, how="outer", on=headings)
    df_base = df_base.drop(len(df_base.index) - 1)
    return df_base


def refined_events_data(data):
    sub_dict = {}
    goal_dict = {}
    goal_counter = 0
    for x in data:
        minute = int(x[0].split("&")[0].split("+")[0])
        event_type = x[-1][2:]
        pen_check = x[-2] == "Penalty Kick"
        if pen_check:
            goal_counter += 1
            goal_dict[minute] = goal_counter - 1, goal_counter
        elif event_type == "Substitute":
            sub_dict.setdefault(x[2], 0)
            sub_dict[x[2]] = minute
        elif event_type[0:4] == "Goal":
            goal_counter += 1
            goal_dict[minute] = goal_counter - 1, goal_counter

    if not goal_dict:
        goals_against = 0
    else:
        last_time = list(goal_dict)[-1]
        goals_against = goal_dict[last_time][1]
    return sub_dict, goal_dict, goals_against


def get_match_events(url):
    soup = get_soup_from_url(url)
    match_data = soup.find("div", {"id": "events_wrap"})
    raw_home_data = match_data.find_all("div", {"class": "event a"})
    home_data = [
        [x.strip() for x in event.text.split("\n") if x != ""]
        for event in raw_home_data
    ]
    raw_away_data = match_data.find_all("div", {"class": "event b"})
    away_data = [
        [x.strip() for x in event.text.split("\n") if x != ""]
        for event in raw_away_data
    ]
    return *refined_events_data(home_data), *refined_events_data(away_data)


def get_expected_data(df):
    xGA_dict = {}
    PSxGA_dict = {}
    for index, row in df.iterrows():
        if isinstance(row["Minute"], str):
            minute = int(row["Minute"].split("+")[0])
        else:
            minute = row["Minute"]
        if math.isnan(minute):
            continue
        cumul_xG = row["Cumul_xG"]
        cumul_PSxG = row["Cumul_PSxG"]
        xGA_dict[minute] = round(cumul_xG - row["xG"], 2), round(cumul_xG, 2)
        if not math.isnan(row["PSxG"]):
            PSxGA_dict[minute] = (
                round(cumul_PSxG - row["PSxG"], 2),
                round(cumul_PSxG, 2),
            )
    return xGA_dict, PSxGA_dict


def get_shot_dataframes(df):
    shots_against_headers = ["Minute", "Player", "xG", "PSxG"]

    df.columns = [x[1] for x in df.columns]
    df = df.iloc[:, 0:5:1]
    df = df[shots_against_headers]
    df["Cumul_xG"] = df["xG"].cumsum(skipna=True)
    df["Cumul_PSxG"] = df["PSxG"].cumsum(skipna=True)
    x_goals, xPS_goals = get_expected_data(df)

    if not x_goals:
        x_goals_against = 0
    else:
        last_time_xG = list(x_goals)[-1]
        x_goals_against = x_goals[last_time_xG][1]

    if not xPS_goals:
        xPS_goals_against = 0
    else:
        last_time_PSxG = list(xPS_goals)[-1]
        xPS_goals_against = xPS_goals[last_time_PSxG][1]

    return x_goals, x_goals_against, xPS_goals, xPS_goals_against


def get_shot_df_info(df):
    PSxG_header = ["Player", "PSxG", "Distance"]

    df = df.iloc[:, 0:9:1]
    df = df[PSxG_header]
    df["Player"] = df.apply(
        lambda row: row["Player"][:-6]
        if isinstance(row["Player"], str) and row["Player"][-6:] == " (pen)"
        else row["Player"],
        axis=1,
    )
    df.columns = ["Player_Info-Player", "Performance-PSxG", "Performance-Distance"]
    df = df.groupby("Player_Info-Player").aggregate(
        {"Performance-PSxG": "sum", "Performance-Distance": "sum"}
    )
    return df


def outer_calc_goals_against(player_dict, ga_dict, default, return_shots=False):
    def inner_calc_goals_against(row):
        name = row["Player_Info-Player"]
        mins = row["Player_Info-Min"]
        sorted_list = list(ga_dict)
        if mins == 90:
            if return_shots:
                return default, len(sorted_list)
            return default
        elif name in player_dict:
            start_min = player_dict[name]
        else:
            start_min = 0
        new_list = slice_list(sorted_list, start_min, start_min + mins)
        if len(new_list) == 0:
            if return_shots:
                return 0, 0
            return 0
        ga = ga_dict[new_list[-1]][1] - ga_dict[new_list[0]][0]
        if return_shots:
            return ga, len(new_list)
        return ga

    return inner_calc_goals_against


def get_team_dataframe(df, shot_df, ga_func, xga_func, PSxga_func):
    df = pd.merge(df, shot_df, how="outer", on="Player_Info-Player")
    df["Goals_Against-Goals_Against"] = df.apply(ga_func, axis=1)
    df["Both"] = df.apply(xga_func, axis=1)
    df[["Goals_Against-xGoals_Against", "Goals_Against-Shots_Faced"]] = pd.DataFrame(
        df["Both"].tolist(), index=df.index
    )
    df = df.drop(["Both"], axis=1)
    df["Goals_Against-PSxGoals_Against"] = df.apply(PSxga_func, axis=1)

    # if FPL_dict:
    #     df['FPL_Position'] = df.apply(lambda row : FPL_dict[row['Player']], axis = 1)

    #
    return df


def match_loader(raw_url):
    url = "https://fbref.com/" + raw_url
    df_list = get_df_list_from_url(url)

    home_main_df = create_main_df(df_list[3:10])
    away_main_df = create_main_df(df_list[10:17])

    (
        home_subs,
        home_goals,
        away_goals_against,
        away_subs,
        away_goals,
        home_goals_against,
    ) = get_match_events(url)

    x_home_goals, x_away_goals_against, PSx_home_goals, PSx_away_goals_against = (
        get_shot_dataframes(df_list[18])
    )
    x_away_goals, x_home_goals_against, PSx_away_goals, PSx_home_goals_against = (
        get_shot_dataframes(df_list[19])
    )

    home_shot_df = get_shot_df_info(df_list[18])
    away_shot_df = get_shot_df_info(df_list[19])

    home_ga_func = outer_calc_goals_against(home_subs, away_goals, home_goals_against)
    home_xga_func = outer_calc_goals_against(
        home_subs, x_away_goals, x_home_goals_against, True
    )
    home_PSxga_func = outer_calc_goals_against(
        home_subs, PSx_away_goals, PSx_home_goals_against
    )

    away_ga_func = outer_calc_goals_against(away_subs, home_goals, away_goals_against)
    away_xga_func = outer_calc_goals_against(
        away_subs, x_home_goals, x_away_goals_against, True
    )
    away_PSxga_func = outer_calc_goals_against(
        away_subs, PSx_home_goals, PSx_away_goals_against
    )

    df_home_stats = get_team_dataframe(
        home_main_df, home_shot_df, home_ga_func, home_xga_func, home_PSxga_func
    )
    df_away_stats = get_team_dataframe(
        away_main_df, away_shot_df, away_ga_func, away_xga_func, away_PSxga_func
    )

    return df_home_stats, df_away_stats


def write_to_csv(team, file_name, df, path):
    match_path = os.path.join(path, team, file_name)
    df.to_csv(match_path, index=False, encoding="utf-8")
    return


def write_match_stats(season, version, verbose=True):
    url_list_url = "https://fbref.com/en/comps/9/{0}/schedule/{0}-Premier-League-Scores-and-Fixtures".format(
        season
    )
    url_list = get_fixture_links(url_list_url)
    team_list_url = "https://fbref.com/en/comps/9/{0}/{0}-Premier-League-Stats".format(
        season
    )
    team_list = get_team_list(team_list_url)

    parent_directory = os.getcwd()
    version_path = os.path.join(parent_directory, "Version-{}".format(version))
    if not os.path.isdir(version_path):
        os.mkdir(version_path)
    season_path = os.path.join(version_path, season)
    if not os.path.isdir(season_path):
        os.mkdir(season_path)
    if verbose:
        start_time = time.time()
    skip_value = 0
    for index, url in enumerate(url_list):
        if verbose:
            t1 = time.time()
        data = url.split("/")[-1]
        *options, month, day, year, _, _ = data.split("-")
        game_date = "{0}-{1}-{2}".format(year, month_dict[month], day)
        home_team, away_team = find_team_names(team_list, options)
        team_check = True
        for team in (home_team, away_team):
            team_path = os.path.join(season_path, team)
            if not os.path.isdir(team_path):
                os.mkdir(team_path)
            file_list = os.listdir(team_path)
            file_name = "{}.csv".format(game_date)
            team_check = team_check and file_name in file_list
        if not team_check:
            home_df, away_df = match_loader(url)
            write_to_csv(home_team, file_name, home_df, season_path)
            write_to_csv(away_team, file_name, away_df, season_path)
            if verbose:
                time_taken = time.time() - t1
                total_time_taken = time.time() - start_time
                print("")
                print(
                    "[{0} of {1}]  Running URL: {2}".format(
                        index + 1, len(url_list), url
                    )
                )
                print("Time Taken: {}".format(round(time_taken)))
                print("Total Time Taken: {}".format(round(total_time_taken)))
                print(
                    "Estimation Completion Time: {}".format(
                        round(
                            (total_time_taken / (index + 1 - skip_value))
                            * (len(url_list) - skip_value)
                        )
                    )
                )
        else:
            if verbose:
                time_taken = time.time() - t1
                total_time_taken = time.time() - start_time
                print("")
                print(
                    "[{0} of {1}] Skipping URL: {2}".format(
                        index + 1, len(url_list), url
                    )
                )
                print("Time Taken: {}".format(round(time_taken)))
                print("Total Time Taken: {}".format(round(total_time_taken)))
                print(
                    "Estimation Completion Time: {}".format(
                        round(
                            (total_time_taken / (index + 1 - skip_value))
                            * (len(url_list) - skip_value)
                        )
                    )
                )
                skip_value += 1
    return


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def choose_name_dict(FPL=False, FLPro=False):
    parent_directory = os.getcwd()
    name_dict_directory = os.path.join(parent_directory, "name-dicts")
    folder_list = []
    with os.scandir(name_dict_directory) as file:
        for item in file:
            if item.is_dir():
                folder_list.append(item.name)
    name_dict_folder_name = user_input_options(
        folder_list, "Choose the name dictionary you want."
    )
    name_dict_folder = os.path.join(name_dict_directory, name_dict_folder_name)

    if FPL:
        FPL_dict_file = os.path.join(
            name_dict_folder, name_dict_folder_name + "-FPL.csv"
        )
        FPL_dict = get_name_dict(FPL_dict_file)
    else:
        FPL_dict = None

    if FLPro:
        FLPro_dict_file = os.path.join(
            name_dict_folder, name_dict_folder_name + "-FLPro.csv"
        )
        FLPro_dict = get_name_dict(FLPro_dict_file)
    else:
        FLPro_dict = None
    return FPL_dict, FLPro_dict


def get_name_dict(file_name):
    name_dict = {}
    with open(file_name, "r", encoding="utf8") as f:
        name_list = f.readlines()
    for i in name_list:
        data = i.split(",")
        name_dict[data[0]] = data[1].strip()
    return name_dict


def calc_FLPro_points(row):
    position = row["Player_Info-FLPro_Position"].strip("*")
    if position in ["GK", "CB", "FB"]:
        clean_sheet = -row["Goals_Against-Goals_Against"]
        if row["Player_Info-Min"] >= 45:
            appearence = 1
            if row["Goals_Against-Goals_Against"] == 0 and row["Player_Info-Min"] >= 75:
                clean_sheet = 2
        else:
            appearence = 0
        return (
            row["Performance-Gls"] * 3
            + row["Performance-Ast"] * 2
            + clean_sheet
            + appearence
        )
    elif position in ["MF", "ST"]:
        return row["Performance-Gls"] * 3 + row["Performance-Ast"] * 2
    else:
        raise PositionError(position)


def calc_FLPro_xPoints(row):
    position = row["Player_Info-FLPro_Position"].strip("*")
    init_points = row["Expected-xG"] * 3 + row["Expected-xAG"] * 2
    if position in ["GK", "CB", "FB"]:
        n = row["Goals_Against-Shots_Faced"]
        if n == 0:
            return init_points
        p = row["Goals_Against-xGoals_Against"] / n
        if row["Player_Info-Min"] >= 45:
            appearence = 1
            if row["Player_Info-Min"] >= 75:
                clean_sheet = 3 * binom.pmf(0, n, p)
            else:
                clean_sheet = 0
        else:
            appearence = 0
            clean_sheet = 0
        for x in range(1, n + 1):
            clean_sheet -= (x - appearence) * binom.pmf(x, n, p)
        return init_points + clean_sheet
    elif position in ["MF", "ST"]:
        return init_points
    else:
        raise PositionError(position)


def outer_clean_sheet_func(pos, ga=None):
    def GK_DF_clean_sheet_func(minute_type):
        if minute_type and ga == 0:
            return 4
        else:
            return -ga // 2

    def MF_clean_sheet_func(minute_type):
        if minute_type and ga == 0:
            return 1
        return 0

    def FW_clean_sheet_func(minute_type):
        return 0

    if pos == "GK" or pos == "DF":
        return GK_DF_clean_sheet_func
    elif pos == "MF":
        return MF_clean_sheet_func
    elif pos == "FW":
        return FW_clean_sheet_func
    else:
        raise PositionError(pos)


def calc_FPL_points(row):
    position = row["Player_Info-FPL_Position"].strip("*")

    gk_points = 0
    if position == "GK":
        goal_points = 10
        cs_func = outer_clean_sheet_func(position, row["Goals_Against-Goals_Against"])
        gk_points = row["Shot Stopping-Saves"] // 3
    elif position == "DF":
        goal_points = 6
        cs_func = outer_clean_sheet_func(position, row["Goals_Against-Goals_Against"])
    elif position == "MF":
        goal_points = 5
        cs_func = outer_clean_sheet_func(position, row["Goals_Against-Goals_Against"])
    elif position == "FW":
        goal_points = 4
        cs_func = outer_clean_sheet_func(position)
    else:
        raise PositionError(position)

    if row["Player_Info-Min"] >= 60:
        cs_points = cs_func(1)
        minute_points = 2
    else:
        cs_points = cs_func(0)
        minute_points = 1

    return (
        minute_points
        + goal_points * (row["Performance-Gls"] - row["Performance-PK"])
        + 3 * row["Performance-Ast"]
        + cs_points
        + gk_points
        - 2 * (row["Performance-PKatt"] - row["Performance-PK"])
        - row["Performance-CrdY"]
        - 3 * row["Performance-CrdR"]
        - 2 * row["Performance-OG"]
    )


def outer_xClean_sheet_func(pos, xGA=None, shots=None):
    def GK_DF_clean_sheet_func(minute_type):
        if shots == 0:
            p = 1
        else:
            p = xGA / shots

        if minute_type:
            init_cs = 4 * binom.pmf(0, shots, p)
        else:
            init_cs = 0

        for x in range(1, shots + 1):
            init_cs -= (x // 2) * binom.pmf(x, shots, p)
        return init_cs

    def MF_clean_sheet_func(minute_type):
        if shots == 0:
            p = 1
        else:
            p = xGA / shots

        if minute_type:
            return binom.pmf(0, shots, p)
        return 0

    def FW_clean_sheet_func(minute_type):
        return 0

    if pos == "GK" or pos == "DF":
        return GK_DF_clean_sheet_func
    elif pos == "MF":
        return MF_clean_sheet_func
    elif pos == "FW":
        return FW_clean_sheet_func
    else:
        raise PositionError(pos)


def calc_FPL_xPoints(row):
    position = row["Player_Info-FPL_Position"].strip("*")

    gk_points = 0
    if position == "GK":
        goal_points = 10
        cs_func = outer_xClean_sheet_func(
            position,
            row["Goals_Against-xGoals_Against"],
            row["Goals_Against-Shots_Faced"],
        )
        gk_points = row["Shot Stopping-Saves"] / 3
    elif position == "DF":
        goal_points = 6
        cs_func = outer_xClean_sheet_func(
            position,
            row["Goals_Against-xGoals_Against"],
            row["Goals_Against-Shots_Faced"],
        )
    elif position == "MF":
        goal_points = 5
        cs_func = outer_xClean_sheet_func(
            position,
            row["Goals_Against-xGoals_Against"],
            row["Goals_Against-Shots_Faced"],
        )
    elif position == "FW":
        goal_points = 4
        cs_func = outer_xClean_sheet_func(position)
    else:
        raise PositionError(position)

    if row["Player_Info-Min"] >= 60:
        cs_points = cs_func(1)
        minute_points = 2
    else:
        cs_points = cs_func(0)
        minute_points = 1
    return (
        minute_points
        + goal_points * (row["Expected-xG"])
        + 3 * row["Expected-xAG"]
        + cs_points
        + gk_points
        - 0.42 * (row["Performance-PKatt"])
        - row["Performance-CrdY"]
        - 3 * row["Performance-CrdR"]
    )


def add_FL_columns(df, FL_dict, FL_func, FL_xfunc, name):
    df["Player_Info-" + name + "_Position"] = df.apply(
        lambda row: FL_dict[row["Player_Info-Player"]], axis=1
    )
    df["Fantasy_Stats-" + name + "_Points"] = df.apply(FL_func, axis=1)
    df["Fantasy_Stats-" + name + "_xPoints"] = df.apply(FL_xfunc, axis=1)
    return df


def add_fl_stats_all_df(season, version, FL_dict, FL_func, FL_xfunc, name):
    parent_directory = os.getcwd()
    season_directory = os.path.join(parent_directory, "Version-" + str(version), season)
    teams = os.listdir(season_directory)
    for team in teams:
        team_directory = os.path.join(season_directory, team)
        matches = os.listdir(team_directory)
        for match in matches:
            match_path = os.path.join(team_directory, match)
            df = pd.read_csv(match_path)
            df = add_FL_columns(df, FL_dict, FL_func, FL_xfunc, name)
            df.to_csv(match_path, index=False, encoding="utf-8")
    return


def get_fantasy_data(season, version, FPL_dict=None, FLPro_dict=None):
    if FPL_dict:
        FPL_func = calc_FPL_points
        FPL_xfunc = calc_FPL_xPoints
        add_fl_stats_all_df(season, version, FPL_dict, FPL_func, FPL_xfunc, "FPL")
    if FLPro_dict:
        FLPro_func = calc_FLPro_points
        FLPro_xfunc = calc_FLPro_xPoints
        add_fl_stats_all_df(
            season, version, FLPro_dict, FLPro_func, FLPro_xfunc, "FLPro"
        )
    return


def add_dataframes(df1, df2, on_titles):
    all_titles = list(df1)
    df3 = pd.merge(df1, df2, how="outer", on=on_titles)
    add_titles = [title for title in all_titles if title not in on_titles]
    for header in all_titles:
        if header in on_titles:
            continue
        df3[header] = df3.loc[:, [header + "_x", header + "_y"]].sum(axis=1)
    return df3[on_titles + add_titles]


def group_team_csv(path, on_titles):
    match_list = os.listdir(path)
    first = True
    for match in match_list:
        if match == "grouped_data.csv":
            continue
        match_path = os.path.join(path, match)
        df = pd.read_csv(match_path)
        df.drop(
            columns=[
                "Player_Info-#",
                "Player_Info-Nation",
                "Player_Info-Pos",
                "Player_Info-Age",
            ],
            inplace=True,
        )

        if first:
            df_base = df
            first = False
        else:
            df_base = add_dataframes(df_base, df, on_titles)
    return df_base


def get_big_df(season, version, FPL=False, FLPro=False):
    on_titles = ["Player_Info-Player"]
    if FPL:
        on_titles.append("Player_Info-FPL_Position")
    if FLPro:
        on_titles.append("Player_Info-FLPro_Position")

    parent_directory = os.getcwd()
    season_directory = os.path.join(parent_directory, "Version-" + str(version), season)
    teams = os.listdir(season_directory)
    first = True
    for team in teams:
        team_directory = os.path.join(season_directory, team)
        team_df = group_team_csv(team_directory, on_titles)

        if first:
            df_base = team_df
            first = False
        else:
            df_base = df_base.append(team_df)

        path = os.path.join(season_directory, "Main_df.csv")

        df_base.to_csv(path, index=False, encoding="utf-8")
    return


# def x(season, version):
#     parent_directory = os.getcwd()
#     season_directory = os.path.join(parent_directory, 'Version-' + str(version), season)
#     teams = os.listdir(season_directory)
#     for team in teams:
#         team_directory = os.path.join(season_directory, team)
#         matches = os.listdir(team_directory)
#         for match in matches:
#             match_path = os.path.join(team_directory, match)
#             with open(match_path, 'r', encoding="utf8") as f:
#                 data = f.readlines()
#             last = data[-1].split(',')[0]
#             if last[-6:] == ' (pen)':
#                 os.remove(match_path)
#     return


def main():
    season = "2024-2025"
    version = 1

    # write_match_stats(season, version)

    # FPL_dict, FLPro_dict = choose_name_dict(FPL = False, FLPro = True)
    # get_fantasy_data(season, version, FLPro_dict = FLPro_dict)

    get_big_df(season, version, FLPro=True)

    # write_match_stats(season, version)

    return


if __name__ == "__main__" or __name__ == "builtins":
    main()
