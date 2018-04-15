import pandas as pd
import sqlite3

from luncheater import LunchEater


DB_CONN_STR = 'example.db'


def list_to_sql_clause(some_list):
    # https://stackoverflow.com/a/283801
    placeholder = '?'
    placeholders = ', '.join(placeholder for item in some_list)
    return placeholders


def get_all_lunches():
    with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select id, lunch, distance
        from lunches
        '''
        df = pd.read_sql(cmd, conn)
        return df


def get_lunches_from_ids(lunch_id_list):
    with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select id, lunch, distance
        from lunches
        where id in ({lil})
        '''.format(lil=list_to_sql_clause(lunch_id_list))
        df = pd.read_sql(cmd, conn, params=lunch_id_list)
        return df


def get_lunches_not_this_week():
     with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select
            id,
            lunch,
            (S.last <= date('now', '-7 day') or S.last is null) avail
        from
        (
            select
                L.id,
                L.lunch,
                max(H.timestamp) last
            from lunches L
            left join history H
                on H.lunchid = L.id
            group by L.lunch, L.id
        ) S
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


def get_ratings(personid=None):
    with sqlite3.connect(DB_CONN_STR) as conn:
        if personid is not None:
            person_condition = 'where personid={p}'.format(p=personid)
        else:
            person_condition = ''
        cmd = '''
        select *
        from ratings
        {pc}
        '''.format(pc=person_condition)
        df = pd.read_sql(cmd, conn)
        return df


def get_all_lunch_eaters():
    with sqlite3.connect(DB_CONN_STR) as conn:
        cmd = '''
        select *
        from people
        '''
        df = pd.read_sql(cmd, conn)

        lunch_eaters = []
        people = df.to_dict(orient='records')
        for p in people:
            lunch_eaters.append(LunchEater(p['id'], p['name']))

        return lunch_eaters


def set_lunch_eater_rating(personid, lunchid, rating):
    with sqlite3.connect(DB_CONN_STR) as conn:
        cursor = conn.cursor()
        cmd = '''
        delete from ratings
        where personid={p}
        and lunchid={l}
        '''.format(p=personid, l=lunchid)
        cursor.execute(cmd)

        cmd = '''
        insert into ratings (lunchid, personid, rating)
        values
        ({l}, {p}, {r})
        '''.format(l=lunchid, p=personid, r=rating)
        cursor.execute(cmd)


def log_lunch(dt, lunchid):
    with sqlite3.connect(DB_CONN_STR) as conn:
        cursor = conn.cursor()
        cmd = '''
        insert into history
        (lunchid, timestamp)
        values
        ({l}, '{d}')
        '''.format(l=lunchid, d=dt.strftime('%Y-%m-%d'))
        cursor.execute(cmd)


def lunchid_to_name(lunchid):
     with sqlite3.connect(DB_CONN_STR) as conn:
        cursor = conn.cursor()
        cmd = '''
        select *
        from lunches
        where id={l}
        '''.format(l=lunchid)
        df = pd.read_sql(cmd, conn)
        return df

