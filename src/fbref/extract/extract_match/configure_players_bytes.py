from io import BytesIO
from typing import List
from bs4.element import Tag


def configure_players_bytes(rows: List[Tag]) -> bytes:
    """
    Convert HTML table rows into CSV-formatted bytes.

    Each row is expected to contain two `<td>` elements: the first for the
    shirt number and the second for the player name. Any `<div>` elements
    inside the player name column will be removed.

    Args:
        rows (List[Tag]): List of BeautifulSoup `<tr>` elements representing
            table rows.

    Returns:
        bytes: CSV content containing "Shirt Number,Player" and one line per row,
            encoded as UTF-8.
    """
    buffer = BytesIO()
    buffer.write("Shirt Number,Player\n".encode("utf-8"))
    for row in rows:
        tds = row.find_all("td")
        if len(tds) == 2:
            shirt_number = tds[0].get_text(strip=True)
            for div in tds[1].find_all("div"):
                div.decompose()
            name = tds[1].get_text(strip=True)
            line = f"{shirt_number},{name}\n"
            buffer.write(line.encode("utf-8"))
    return buffer.getvalue()
