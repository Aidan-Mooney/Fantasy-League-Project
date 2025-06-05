def list_to_csv(headings, rows=[]):
    csv_string = ""
    csv_string += ",".join(headings) + "\n"
    for row in rows:
        csv_string += ",".join(row) + "\n"
    return csv_string
