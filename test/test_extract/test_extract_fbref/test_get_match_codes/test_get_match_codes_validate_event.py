from pytest import raises


from extract.extract_fbref.get_match_codes import validate_event


def test_validate_event_returns_none():
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
    }
    assert validate_event(test_event) is None


def test_validate_event_raises_error_if_event_is_not_a_dict():
    test_event = []
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must be a dictionary"


def test_validate_event_raises_error_if_template_or_league_or_season_is_wrong_type():
    test_template = 0
    test_league = "Premier-League"
    test_season = 2025
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "template value must be a string"

    test_template = "template"
    test_league = 0
    test_season = 2025
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "league value must be a string"

    test_template = "template"
    test_league = "Premier-League"
    test_season = "2025"
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "season value must be an int"


def test_validate_event_raises_type_error_if_event_has_a_missing_key():
    test_event = {}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season'}"
    )

    test_event = {"league": "Premier-League"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season'}"
    )

    test_event = {"season": "2025"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season'}"
    )

    test_event = {"template": "test"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season'}"
    )


def test_validate_event_raises_type_error_if_event_has_an_extra_key():
    test_event = {
        "template": "test",
        "league": "Premier-League",
        "season": 2025,
        "what": "what",
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season'}"
    )
