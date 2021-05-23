import os
import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import arrow
import acp_times
import config

import logging

app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

@app.route('/')
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


@app.route("/new", methods=['POST'])
def new():

    app.logger.debug("Post request: {}".format(request.form))

    db.tododb.drop()
    app.logger.debug("Database collection deleted")

    item_doc = {}

    for item in request.form:
        app.logger.debug("item {}".format(item))
        item_doc[item] = []
        for data in request.form.getlist(item):
            app.logger.debug("data {}".format(data))
            if len(data) > 0:
                item_doc[item].append(data)


    app.logger.debug("item_doc {}".format(item_doc))
    db.tododb.insert_one(item_doc)

    # Entered an empty form, drop whatever incomplete data was there
    # KM must always be filled out (automatic or manually) for successful form submission
    if len(item_doc['km']) == 0:
        db.tododb.drop()
        return flask.render_template('empty.html')

    return redirect(url_for('index'))

@app.route("/display", methods=['POST'])
def display():
    # re-formatting db data for easier processing (to make data iterable) in todo.html file
    # (1) get ids from db
    ids = []
    for entry in db.tododb.find():
        for id in entry:
            # keep the unique ids, if we've repeated ourselves, we're on a new entry
            if id in ids:
                break
            # don't need the _id field
            elif str(id) != "_id":
                app.logger.debug("id={}".format(id))
                ids.append(id)

    app.logger.debug("ids={}".format(ids))

    # (2) add values from each id in db to dictionary
    items = {}
    for id in ids:
        items[id] = []
        id_vals = db.tododb.distinct(id)
        for i in range(len(id_vals)):
            items[id].append(id_vals[i])

    app.logger.debug("items={}".format(items))

    # Trying to display empty DB
    if len(items) == 0:
        db.tododb.drop()
        return flask.render_template('empty.html')


    return flask.render_template('todo.html', items=items)



###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', 999, type=int)
    begin_date = request.args.get('begin_date', 999, type=str)
    begin_time = request.args.get('begin_time', 999, type=str)

    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet_dist_km={}".format(brevet_dist_km))
    app.logger.debug("begin_date={}".format(begin_date))
    app.logger.debug("begin_time={}".format(begin_time))
    app.logger.debug("request.args: {}".format(request.args))

    brevet_start_time = begin_date + " " + begin_time

    app.logger.debug("brevet_start_time={}".format(brevet_start_time))

    open_time = acp_times.open_time(km, brevet_dist_km, brevet_start_time)
    close_time = acp_times.close_time(km, brevet_dist_km, brevet_start_time)

    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
