from datetime import datetime
import pandas as pd
import sqlite3


def change_date_range(df, time_div):
    if time_div == 'weeks':
        time_format = '%Y-%W'
    elif time_div == 'months':
        time_format = '%Y-%m'
    else:
        time_format = '%Y-%m-%d'

    df['timestamp'] = df['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime(time_format))
    df = df.groupby('timestamp').mean().reset_index()
    return df


class DataManager:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)

    def return_connection(self):
        return self.conn

    def tree(self):
        return pd.read_sql_query("select name from sqlite_master where type='table'", self.conn)

    def table_info(self, table_name):
        return self.query('PRAGMA table_info({});'.format(table_name))

    def query(self, query):
        return pd.read_sql_query(query, self.conn)

    def load_table(self, table_name):
        return pd.read_sql_query('select * from {}'.format(table_name), self.conn)

    def save_table(self, df, table_name, mode=''):
        # mode = replace/append
        mode = 'append' if len(mode) == 0 else mode
        df.to_sql(table_name, self.conn, if_exists=mode, index=False)
        print('{} saved (mode: {})'.format(table_name, mode))

    def remove_table(self, table_name):
        cur = self.conn.cursor()
        cur.execute('drop table {}'.format(table_name))
        print('{} removed'.format(table_name))