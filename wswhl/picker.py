from collections import defaultdict 
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

from config import grubholes, preferences


HISTORY_FILE = r'lunches.history'
REPEAT_WINDOW_LIMIT = 7


def read_csv(f, parse_dates=[]):
    df = pd.read_csv(f, parse_dates=parse_dates)
    return df


def get_date_window(dt, window_size):
    window = [dt - timedelta(days=n) for n in range(1,window_size + 1)]
    return window


def aggregate_preferences(missing=[]):
    result = defaultdict(list)
    for name, weights in preferences.items():
        if name not in missing:
            for lunch, weight in weights.items():
                result[lunch].append(weight)

    result = {k: np.mean(v) for k, v in result.items()}

    return result


def get_lunch_weightings(lunches):
    weights = aggregate_preferences()

    # TODO combine days since into this weighting

    probs = {k: v for k, v in weights.items() if k in lunches['lunch'].values}
    return probs


def pick_a_lunch(absentees=[]):
    dt = date.today()
    history = read_csv(HISTORY_FILE, parse_dates=['date'])
    available_lunches = [*grubholes]
    last_week = get_date_window(dt, REPEAT_WINDOW_LIMIT - 1)
    last_week_idx = history['date'].isin(last_week)
    last_week_lunches = history.loc[last_week_idx, 'lunch'].values

    lunches = pd.DataFrame({
        'lunch': [l for l in available_lunches if l not in last_week_lunches]
        })
    lunches['last'] = lunches['lunch'].apply(
            lambda l: max(history['date'].where(history['lunch'] == l))
            ).fillna(date(1970, 1, 1))
    lunches['dayssince'] = (dt - lunches['last']).dt.days

    weight_map = get_lunch_weightings(lunches)
    lunches['weight'] = lunches['lunch'].map(weight_map)

    weight_sd = np.nanstd(lunches['weight'])
    weight_mean = np.nanmean(lunches['weight'])
    default_value = max(0, weight_mean - (2 * weight_sd))
    lunches['weight'].fillna(default_value, inplace=True)

    lunches['weight'] = lunches['weight'] / lunches['weight'].sum()
    import pdb; pdb.set_trace()

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

