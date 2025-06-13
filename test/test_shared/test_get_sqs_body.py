import json


from get_sqs_body import get_sqs_body


def test_get_sqs_body_returns_a_list_of_dicts():
    test_event = {
        "Records": [
            {"body": '{"key1": "value1", "key2": "value2"}'},
            {"body": '{"key3": "value3"}'},
        ]
    }
    result = get_sqs_body(test_event)
    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, dict)


def test_get_sqs_body_returns_an_empty_list_when_passed_an_empty_event():
    test_event = {"Records": []}
    result = get_sqs_body(test_event)
    assert len(result) == 0


def test_get_sqs_body_returns_one_body_of_a_response_with_one_item():
    test_dict = {"test_event": "im a value", "test_testies": 2}
    test_body = json.dumps(test_dict)
    test_event = {
        "Records": [
            {"body": test_body},
        ]
    }
    result = get_sqs_body(test_event)
    assert len(result) == 1
    assert result[0] == test_dict


def test_get_sqs_body_returns_many_bodies():
    records = []
    for i in range(5):
        test_dict = {"test_event": i}
        records.append({"body": json.dumps(test_dict)})
    test_event = {"Records": records}
    result = get_sqs_body(test_event)
    for index, j in enumerate(result):
        assert j == {"test_event": index}
