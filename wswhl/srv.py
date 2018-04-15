from flask import Flask, render_template, request
from flask_scss import Scss


import db
import picker


app = Flask(__name__)
app.debug = True
Scss(app)


@app.route('/', methods=['GET', 'POST'])
def lunch_app():
    people = db.get_all_lunch_eaters()
    lunches = db.get_lunches_not_this_week().to_dict(orient='records')

    if request.method == 'GET':
        return render_template('index.html', people=people, lunches=lunches)

    if request.method == 'POST':
        data = request.form
        for p in people:
            p.avail = data.get('cp_{}'.format(p.dbid), 'off') == 'on'

        lunch_ids = []
        for l in [lunch for lunch in lunches if lunch['avail']]:
            enabled = False
            enabled = data.get('cl_{}'.format(l['id']), 'off') == 'on'
            if enabled:
                lunch_ids.append(l['id'])

        lunches = db.get_lunches_from_ids(lunch_ids)
        the_lunch = picker.pick_a_lunch(lunches, people)
        return render_template('lunch.html', lunch=the_lunch['lunch'])



if __name__ == '__main__':
    app.run()

