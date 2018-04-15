from collections import defaultdict 
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

import db
import luncheater


def aggregate_preferences(lunch_eaters):
    # TODO currently we normalize all lunches, then strip out the unavailable
    # lunches over in get_lunch_weightings. Probably more fair to normalize
    # within the set of valid ratings only.

    # aggregate all lunch eaters' normalized ratings
    all_ratings = pd.concat(list(map(
            lambda le: le.get_normalized_ratings(),
            lunch_eaters)))
    averaged = all_ratings.groupby('lunchid') \
                          .aggregate(np.mean)
    result = averaged.to_dict()['rating']

    return result


def get_lunch_weightings(lunches, lunch_eaters):
    lunch_eaters_attending = [l for l in lunch_eaters if l.avail]
    weights = aggregate_preferences(lunch_eaters_attending)

    probs = {k: v for k, v in weights.items() if k in lunches['id'].values}
    return probs


def pick_a_lunch(lunches, lunch_eaters):
    """
    Answers the question: Where Shall We Have Lunch?

    Arguments:
        lunches: pd.DataFrame(id, lunch) representing luncheries
        lunch_eaters: [LunchEater] them who want to eat

    Returns:
        pd.DataFrame(id, lunch, ... )

    TODO Return an object with a message, lunch name, and lunch id
    This would allow the print of 'You have already chosen' to be more
    compatible with e.g. Flask srv

    TODO Where should logging occur? From here or from the calling function?
    E.g. where does Flask log from?
    """
    dt = date.today()
    history = db.get_all_history()
    todays_lunch = history['timestamp'] == dt
    if todays_lunch.any():
        print('You have already chosen.')
        lunchid = history.loc[todays_lunch, 'lunchid'].values[0]
        return db.lunchid_to_df(lunchid)

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

    # renormalize weights to between 0 and 1
    lunches['weight'] /= lunches['weight'].sum()

    draw = np.random.choice(lunches.index, 1, p=lunches['weight'])[0]
    return lunches.loc[draw]


def main():
    lunches = db.get_all_lunches()
    lunch_eaters = db.get_all_lunch_eaters()
    lunch = pick_a_lunch(lunches, lunch_eaters)
    db.log_lunch(dt, lunch['id']);
    print(lunch['lunch'])

if __name__ == '__main__':
    main()

