def get_table_data(table):
    rows = table.findAll(lambda tag: tag.name == "tr")
    return rows
