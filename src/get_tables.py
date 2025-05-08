def get_tables(soup):
    tables = soup.find_all(lambda tag: tag.name == "table")
    return tables
