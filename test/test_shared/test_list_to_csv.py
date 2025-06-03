from list_to_csv import list_to_csv


def test_list_to_csv_returns_a_string():
    headings = ("heading1", "heading2")
    rows = [("row1a", "row1b"), ("row2a", "row2b"), ("row3a", "row3b")]
    result = list_to_csv(headings, rows)
    assert isinstance(result, str)


def test_list_to_csv_returns_one_heading_with_no_rows():
    headings = ("heading",)
    result = list_to_csv(headings)
    expected = "heading\n"
    assert result == expected


def test_list_to_csv_returns_multiple_headings_no_rows():
    headings = ("heading1", "heading2", "heading3")
    result = list_to_csv(headings)
    expected = "heading1,heading2,heading3\n"
    assert result == expected


def test_list_to_csv_returns_multiple_headings_with_one_row():
    headings = ("heading1", "heading2", "heading3")
    rows = [("row1a", "row1b", "row1c")]
    result = list_to_csv(headings, rows)
    expected = "heading1,heading2,heading3\n" + "row1a,row1b,row1c\n"
    assert result == expected


def test_list_to_csv_returns_multiple_headings_with_multiple_rows():
    headings = ("heading1", "heading2", "heading3")
    rows = [
        ("row1a", "row1b", "row1c"),
        ("row2a", "row2b", "row2c"),
        ("row3a", "row3b", "row3c"),
        ("row4a", "row4b", "row4c"),
    ]
    result = list_to_csv(headings, rows)
    expected = (
        "heading1,heading2,heading3\n"
        + "row1a,row1b,row1c\n"
        + "row2a,row2b,row2c\n"
        + "row3a,row3b,row3c\n"
        + "row4a,row4b,row4c\n"
    )
    assert result == expected
