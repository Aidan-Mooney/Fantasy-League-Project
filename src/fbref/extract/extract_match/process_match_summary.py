from fbref.extract.extract_match.process_team_summary import process_team_summary


def process_match_summary(bucket, template, league, season, fixture_id, soup):
    match_data = soup.find("div", {"id": "events_wrap"})
    process_team_summary(
        bucket, template, league, season, fixture_id, match_data, "home"
    )
    process_team_summary(
        bucket, template, league, season, fixture_id, match_data, "away"
    )
