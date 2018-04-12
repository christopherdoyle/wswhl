import pandas as pd
import sqlite3


DB_CONN_STR = 'example.db'


def get_all_lunches():
    with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select id, lunch, distance
        from lunches
        '''
        df = pd.read_sql(cmd, conn)
        return df


def get_all_history():
    with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select *
        from history
        '''
        df = pd.read_sql(cmd, conn, parse_dates=['timestamp'])
        return df

def get_all_ratings():
    with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select *
        from ratings
        '''
        df = pd.read_sql(cmd, conn)
        return df

