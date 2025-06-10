from pytest import raises


from extract.extract_fbref.extract_match import validate_event


def test_validate_event_returns_none():
    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_id = "12345678"
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
        "fixture_id": test_id,
    }
    assert validate_event(test_event) is None


def test_validate_event_raises_error_if_event_is_not_a_dict():
    test_event = []
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must be a dictionary"


def test_validate_event_raises_error_if_any_key_is_the_wrong_type():
    test_template = ["template"]
    test_league = "Premier-League"
    test_season = 2025
    test_id = "12345678"
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
        "fixture_id": test_id,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "template value must be a string"

    test_template = "template"
    test_league = 0
    test_season = 2025
    test_id = "12345678"
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
        "fixture_id": test_id,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "league value must be a string"

    test_template = "template"
    test_league = "Premier-League"
    test_season = "2025"
    test_id = "12345678"
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
        "fixture_id": test_id,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "season value must be an int"

    test_template = "template"
    test_league = "Premier-League"
    test_season = 2025
    test_id = 12345678
    test_event = {
        "template": test_template,
        "league": test_league,
        "season": test_season,
        "fixture_id": test_id,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "fixture_id value must be a string"


def test_validate_event_raises_type_error_if_event_has_a_missing_key():
    test_event = {}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
    )

    test_event = {"league": "Premier-League"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
    )

    test_event = {"season": "2025"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
    )


def test_validate_event_raises_type_error_if_event_has_an_extra_key():
    test_event = {
        "template": "template",
        "league": "Premier-League",
        "season": "2025",
        "fixture_id": "12345678",
        "what": "what",
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert (
        str(f.value)
        == "event must contain only the keys {'template', 'league', 'season', 'fixture_id'}"
    )
