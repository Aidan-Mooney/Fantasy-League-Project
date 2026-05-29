from log_json import log_json
from requests.exceptions import HTTPError
from botocore.exceptions import ClientError
from fbref.extract.get_process_codes.get_processed_codes import get_processed_codes
from fbref.extract.process_league_season_table.process_league_season_table import (
    process_league_season_table,
)
from fbref.extract.extract_match.extract_match import extract_match


def fbref_extract(template: str, league: str, season: int) -> None:
    try:
        processed_ids = get_processed_codes(template, league, season)
        fixture_ids = process_league_season_table(template, league, season)
        for fixture_id in fixture_ids:
            if fixture_id not in processed_ids:
                extract_match(template, league, season, fixture_id)
    except HTTPError as err:
        log_json(err)
    except ClientError as err:
        log_json(err)
    except Exception as err:
        log_json(err)
