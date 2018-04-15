from collections import defaultdict 
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

import db
import luncheater


HISTORY_FILE = r'lunches.history'
REPEAT_WINDOW_LIMIT = 7


def read_csv(f, parse_dates=[]):
    df = pd.read_csv(f, parse_dates=parse_dates)
    return df


def get_date_window(dt, window_size):
    window = [dt - timedelta(days=n) for n in range(1,window_size + 1)]
    return window


def aggregate_preferences(lunch_eaters):
    # aggregate all lunch eaters' normalized ratings
    all_ratings = pd.concat(list(map(
            lambda le: le.get_normalized_ratings(),
            lunch_eaters)))
    averaged = all_ratings.groupby('lunchid') \
                          .aggregate(np.mean)
    result = averaged.to_dict()['rating']

    return result


def get_lunch_weightings(lunches, lunch_eaters):
    weights = aggregate_preferences(lunch_eaters)

    probs = {k: v for k, v in weights.items() if k in lunches['id'].values}
    return probs


def pick_a_lunch(absentees=[]):
    dt = date.today()
    history = db.get_all_history()
    lunches = db.get_all_lunches()
    lunch_eaters = db.get_all_lunch_eaters()

    last_visited = history.groupby('lunchid').agg(max)
    last_visited.rename(columns={'timestamp': 'last_visited'}, inplace=True)
    lunches = lunches.join(last_visited, on='id')
    lunches['last_visited'].fillna(datetime(2018, 1, 1), inplace=True)
    lunches['dayssince'] = (dt - lunches['last_visited']).dt.days
    lunches = lunches[lunches['dayssince'] >= 7]

    weight_map = get_lunch_weightings(lunches, lunch_eaters)
    lunches['weight'] = lunches['id'].map(weight_map)

    weight_sd = np.nanstd(lunches['weight'])
    weight_mean = np.nanmean(lunches['weight'])
    default_value = max(0, weight_mean - (2 * weight_sd))
    lunches['weight'].fillna(default_value, inplace=True)

    # normalize weights to between 0 and 1
    lunches['weight'] /= lunches['weight'].sum()

    draw = np.random.choice(lunches['lunch'], 1, p=lunches['weight'])[0]
    print(draw)


def print_last_week():
    dt = date.today()
    history = read_csv(HISTORY_FILE, parse_dates=['date'])
    last_week = get_date_window(dt, REPEAT_WINDOW_LIMIT - 1)
    last_week_idx = history['date'].isin(last_week)
    last_week = history[last_week_idx]
    print(last_week) 


if __name__ == '__main__':
    pick_a_lunch()

