from bs4 import BeautifulSoup
from pytest import fixture

from fbref.extract.extract_match.html_table_to_csv_bytes import html_table_to_csv_bytes


@fixture(scope="function")
def soup_input_helper():
    def _setup(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("table")

    return _setup


def test_html_table_to_csv_bytes_returns_bytes(soup_input_helper):
    input_html = """
    <table>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
            <tr><td>Row2A</td><td>Row2B</td></tr>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    result = html_table_to_csv_bytes(input_val, ["ColA", "ColB"])
    assert isinstance(result, bytes)


def test_html_table_to_csv_bytes_returns_table_with_headers_and_no_rows_correctly(
    soup_input_helper,
):
    input_html = """
    <table>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    expected = b"ColA,ColB\n"
    result = html_table_to_csv_bytes(input_val, ["ColA", "ColB"])
    assert result == expected


def test_html_table_to_csv_bytes_returns_table_with_headers_and_one_row_correctly(
    soup_input_helper,
):
    input_html = """
    <table>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    expected = b"ColA,ColB\nRow1A,Row1B\n"
    result = html_table_to_csv_bytes(input_val, ["ColA", "ColB"])
    assert result == expected


def test_html_table_to_csv_bytes_returns_table_with_headers_and_multiple_rows_correctly(
    soup_input_helper,
):
    input_html = """
    <table>
        <thead>
            <tr><th>ColA</th><th>ColB</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td></tr>
            <tr><td>Row2A</td><td>Row2B</td></tr>
            <tr><td>Row3A</td><td>Row3B</td></tr>
            <tr><td>Row4A</td><td>Row4B</td></tr>
            <tr><td>Row5A</td><td>Row5B</td></tr>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    expected = (
        b"ColA,ColB\nRow1A,Row1B\nRow2A,Row2B\nRow3A,Row3B\nRow4A,Row4B\nRow5A,Row5B\n"
    )
    result = html_table_to_csv_bytes(input_val, ["ColA", "ColB"])
    assert result == expected


def test_html_table_to_csv_bytes_returns_table_with_two_dimensional_headers_correctly(
    soup_input_helper,
):
    input_html = """
    <table>
        <thead>
            <tr>
                <th colspan="2"></th>
                <th colspan="2">Group Alpha</th>
                <th colspan="2">Group Beta</th>
            </tr>
            <tr>
                <th>ColA</th>
                <th>ColB</th>
                <th>ColC</th>
                <th>ColD</th>
                <th>ColE</th>
                <th>ColF</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Row1A</td>
                <td>Row1B</td>
                <td>Row1C</td>
                <td>Row1D</td>
                <td>Row1E</td>
                <td>Row1F</td>
            </tr>
            <tr>
                <td>Row2A</td>
                <td>Row2B</td>
                <td>Row2C</td>
                <td>Row2D</td>
                <td>Row2E</td>
                <td>Row2F</td>
            </tr>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    expected = (
        b"ColA,ColB,Group Alpha ColC,Group Alpha ColD,Group Beta ColE,Group Beta ColF\n"
        b"Row1A,Row1B,Row1C,Row1D,Row1E,Row1F\n"
        b"Row2A,Row2B,Row2C,Row2D,Row2E,Row2F\n"
    )
    result = html_table_to_csv_bytes(
        input_val,
        [
            "ColA",
            "ColB",
            "Group Alpha ColC",
            "Group Alpha ColD",
            "Group Beta ColE",
            "Group Beta ColF",
        ],
    )
    assert result == expected


def test_html_table_to_csv_bytes_returns_table_with_one_requested_col(
    soup_input_helper,
):
    input_html = """
    <table>
        <thead>
            <tr><th>ColA</th><th>ColB</th><th>ColC</th><th>ColD</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td><td>Row1C</td><td>Row1D</td></tr>
            <tr><td>Row2A</td><td>Row2B</td><td>Row2C</td><td>Row2D</td></tr>
            <tr><td>Row3A</td><td>Row3B</td><td>Row3C</td><td>Row3D</td></tr>
            <tr><td>Row4A</td><td>Row4B</td><td>Row4C</td><td>Row4D</td></tr>
            <tr><td>Row5A</td><td>Row5B</td><td>Row5C</td><td>Row5D</td></tr>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    input_col = ["ColA"]
    expected = b"ColA\nRow1A\nRow2A\nRow3A\nRow4A\nRow5A\n"
    result = html_table_to_csv_bytes(input_val, input_col)
    assert result == expected


def test_html_table_to_csv_bytes_returns_table_with_many_requested_cols(
    soup_input_helper,
):
    input_html = """
    <table>
        <thead>
            <tr><th>ColA</th><th>ColB</th><th>ColC</th><th>ColD</th></tr>
        </thead>
        <tbody>
            <tr><td>Row1A</td><td>Row1B</td><td>Row1C</td><td>Row1D</td></tr>
            <tr><td>Row2A</td><td>Row2B</td><td>Row2C</td><td>Row2D</td></tr>
            <tr><td>Row3A</td><td>Row3B</td><td>Row3C</td><td>Row3D</td></tr>
            <tr><td>Row4A</td><td>Row4B</td><td>Row4C</td><td>Row4D</td></tr>
            <tr><td>Row5A</td><td>Row5B</td><td>Row5C</td><td>Row5D</td></tr>
        </tbody>
    </table>
    """
    input_val = soup_input_helper(input_html)
    input_col = ["ColA", "ColB"]
    expected = (
        b"ColA,ColB\nRow1A,Row1B\nRow2A,Row2B\nRow3A,Row3B\nRow4A,Row4B\nRow5A,Row5B\n"
    )
    result = html_table_to_csv_bytes(input_val, input_col)
    assert result == expected
