import pandas as pd
from io import StringIO


def soup_table_to_df(table):
    df = pd.read_html(StringIO(str(table)))[0]
    return df
