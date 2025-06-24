from pytest import raises


from extract.extract_fbref.sqs_input import validate_event


def test_validate_event_returns_none():
    test_events = [{"test": "event"}]
    test_func_name = "func_name"
    test_event = {
        "events": test_events,
        "func_name": test_func_name,
    }
    assert validate_event(test_event) is None


def test_validate_event_raises_error_if_event_is_not_a_dict():
    test_event = []
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must be a dictionary"


def test_validate_event_raises_error_if_events_or_func_name_is_wrong_type():
    test_events = "test"
    test_func_name = "func_name"
    test_event = {
        "events": test_events,
        "func_name": test_func_name,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "events value must be a list"

    test_events = [{"test": "event"}]
    test_func_name = ["func_name"]
    test_event = {
        "events": test_events,
        "func_name": test_func_name,
    }
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "func_name value must be a string"


def test_validate_event_raises_type_error_if_event_has_a_missing_key():
    test_event = {}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must contain only the keys {'events', 'func_name'}"

    test_event = {"events": [{"test": "event"}]}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must contain only the keys {'events', 'func_name'}"

    test_event = {"func_name": "test_name"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must contain only the keys {'events', 'func_name'}"


def test_validate_event_raises_type_error_if_event_has_an_extra_key():
    test_events = [{"test": "event"}]
    test_func_name = "func_name"
    test_event = {"events": test_events, "func_name": test_func_name, "what": "who"}
    with raises(TypeError) as f:
        validate_event(test_event)
    assert str(f.value) == "event must contain only the keys {'events', 'func_name'}"
