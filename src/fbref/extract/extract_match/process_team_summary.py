from fbref.extract.extract_match.extract_summary import extract_summary
from fbref.extract.save_table_bytes import save_table_bytes


def process_team_summary(
    bucket, template, league, season, fixture_id, match_data, team_side
):
    card_bytes, sub_bytes = extract_summary(match_data, team_side)
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/cards.csv",
        card_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="cards",
    )
    save_table_bytes(
        bucket,
        f"{template}/{league}/{season - 1}-{season}/{fixture_id}/{team_side}/subs.csv",
        sub_bytes,
        template=template,
        league=league,
        season=season,
        fixture_id=fixture_id,
        team_side=team_side,
        table_name="subs",
    )
