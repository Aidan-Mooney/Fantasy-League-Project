from io import BytesIO
from bs4 import BeautifulSoup


def html_table_to_csv_bytes(
    table: BeautifulSoup, cols: list[str] | None = None
) -> bytes:
    """
    Convert an HTML <table> element into a CSV-encoded bytes object.

    Args:
        table (BeautifulSoup): A <table> element parsed by BeautifulSoup.
        cols (list[str] | None): Optional list of column names to include.
            If None, all columns will be included.

    Returns:
        bytes: UTF-8 encoded CSV string representing the table.

    Notes:
        - Supports single-row and two-row headers (with colspan).
        - If `cols` is provided, only matching headers (and their corresponding
          columns) are included in the output.
    """
    if cols is None:
        cols = []

    csv_bytes = BytesIO()
    header_rows = table.find("thead").find_all("tr")

    ignore_rows = []
    expanded_top = []
    if len(header_rows) == 2:
        top_row = header_rows[0]
        for th in top_row.find_all("th"):
            colspan = int(th.get("colspan", 1))
            text = th.get_text(strip=True)
            expanded_top.extend([text] * colspan)

    headings = []
    for index, th in enumerate(header_rows[-1].find_all("th")):
        normal_col = th.get_text(strip=True)
        if len(header_rows) == 2:
            top_col = expanded_top[index]
            heading = f"{top_col} {normal_col}".strip() if top_col else normal_col
        else:
            heading = normal_col
        if cols and heading not in cols:
            ignore_rows.append(index)
            continue
        headings.append(heading)

    csv_bytes.write((",".join(headings) + "\n").encode("utf-8"))

    for tr in table.find("tbody").find_all("tr"):
        row_cells = []
        for index, cell in enumerate(tr.find_all(["td", "th"])):
            if index not in ignore_rows:
                row_cells.append(cell.get_text(strip=True))
        csv_bytes.write((",".join(row_cells) + "\n").encode("utf-8"))

    return csv_bytes.getvalue()
