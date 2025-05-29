from bs4 import BeautifulSoup
from pytest import fixture


from extract.extract_fbref.extract_match import html_table_to_csv_string


@fixture(scope="function")
def soup_input_helper():
    def _setup(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("table")

    return _setup


def test_html_table_to_csv_string_returns_a_string(soup_input_helper):
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
    result = html_table_to_csv_string(input_val)
    assert isinstance(result, str)


def test_html_table_to_csv_string_returns_table_with_headers_and_no_rows_correctly(
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
    expected = "ColA,ColB\n"
    result = html_table_to_csv_string(input_val)
    assert result == expected


def test_html_table_to_csv_string_returns_table_with_headers_and_one_row_correctly(
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
    expected = "ColA,ColB\nRow1A,Row1B\n"
    result = html_table_to_csv_string(input_val)
    assert result == expected


def test_html_table_to_csv_string_returns_table_with_headers_and_multiple_rows_correctly(
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
        "ColA,ColB\n"
        + "Row1A,Row1B\n"
        + "Row2A,Row2B\n"
        + "Row3A,Row3B\n"
        + "Row4A,Row4B\n"
        + "Row5A,Row5B\n"
    )
    result = html_table_to_csv_string(input_val)
    assert result == expected


def test_html_table_to_csv_string_returns_table_with_two_dimensional_headers_correctly(
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
        "ColA,ColB,Group Alpha ColC,Group Alpha ColD,Group Beta ColE,Group Beta ColF\n"
        + "Row1A,Row1B,Row1C,Row1D,Row1E,Row1F\n"
        + "Row2A,Row2B,Row2C,Row2D,Row2E,Row2F\n"
    )
    result = html_table_to_csv_string(input_val)
    print(result)
    assert result == expected


def test_html_table_to_csv_string_returns_table_with_one_requested_col(
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
    expected = "ColA\n" + "Row1A\n" + "Row2A\n" + "Row3A\n" + "Row4A\n" + "Row5A\n"
    result = html_table_to_csv_string(input_val, input_col)
    assert result == expected


def test_html_table_to_csv_string_returns_table_with_many_requested_cols(
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
        "ColA,ColB\n"
        + "Row1A,Row1B\n"
        + "Row2A,Row2B\n"
        + "Row3A,Row3B\n"
        + "Row4A,Row4B\n"
        + "Row5A,Row5B\n"
    )
    result = html_table_to_csv_string(input_val, input_col)
    assert result == expected
