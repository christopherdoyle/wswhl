import db


class LunchEater(object):

    def __init__(self, dbid, name):
        self.avail = True
        self.dbid = dbid
        self.name = name
        self.ratings = db.get_ratings(dbid);

    def get_rating(self, lunchery):
        pass

    def get_normalized_ratings(self):
        nr = self.ratings.copy()
        nr['rating'] /= nr['rating'].sum()
        return nr

    def set_rating(self, lunchid, value):
        db.set_lunch_eater_rating(self.dbid, lunchid, value)
        self.ratings = db.get_ratings(dbid)

