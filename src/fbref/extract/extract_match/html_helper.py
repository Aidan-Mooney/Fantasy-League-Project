from io import BytesIO


def html_helper(rows):
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
