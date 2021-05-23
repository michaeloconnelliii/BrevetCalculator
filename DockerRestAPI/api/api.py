# API Backend- handles retrieving requested data from database

import pymongo
import logging
import flask
import pandas
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('db', 27017)
db = client.tododb


class AllTimes(Resource):
    def get(self):
        path = request.path
        json_times = db.tododb.find_one( {}, { 'open' : 1 , 'close' : 1, '_id' : 0} )
        csv_times = json_to_csv(json_times)
        if 'csv' in path:
            return csv_times
        else:
            return json_times

api.add_resource(AllTimes, "/listAll/", "/listAll/json", "/listAll/csv")

class OpenTimes(Resource):
    def get(self):
        path = request.path
        json_times = db.tododb.find_one( {}, { 'open' : 1 , '_id' : 0} )
        top_n_times = request.args.get('top')
        if top_n_times != None:
            json_times['open'] = json_times['open'][-int(top_n_times):]
        csv_times = json_to_csv(json_times)
        if 'csv' in path:
            return csv_times
        else:
            return json_times

api.add_resource(OpenTimes, "/listOpenOnly/", "/listOpenOnly/json", "/listOpenOnly/csv")

class CloseTimes(Resource):
    def get(self):
        path = request.path
        json_times = db.tododb.find_one( {}, { 'close' : 1 , '_id' : 0} )
        top_n_times = request.args.get('top')
        if top_n_times != None:
            json_times['close'] = json_times['close'][-int(top_n_times):]
        csv_times = json_to_csv(json_times)
        if 'csv' in path:
            return csv_times
        else:
            return json_times

api.add_resource(CloseTimes, "/listCloseOnly/", "/listCloseOnly/json", "/listCloseOnly/csv")

def json_to_csv(json_dict):
    # df is a DataFrame obj.
    df = pandas.DataFrame.from_dict(json_dict)
    csv_string = df.to_csv(header=False, index=False, line_terminator=',')
    # last character in string is a line terminator, remove it
    csv_string = csv_string[:-1]
    return csv_string


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
