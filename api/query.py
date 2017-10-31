from flask_restful import Resource, reqparse
from flask import current_app as app, request
import json
import os
import dateutil.parser
import quasardb

import datetime as dt
from datetime import timedelta, date
import time


def json_serializer(obj):
    if isinstance(obj, date):
        return time.mktime(obj.timetuple()) * 1000
    raise TypeError ("Type %s not serializable" % type(obj))

class QueryCtrl(Resource):

    def get(self):
        return {'message' : '[GET] is not supported'}

    def post(self):
        body = json.loads(request.data)
        range_ = body.get('range', None)
        targets = body.get('targets', None)

        if range_ != None and targets != None:
            from_ = range_.get('from', None)
            to_ = range_.get('to', None)
            # range1start = dateutil.parser.parse(from_)
            # range1end = dateutil.parser.parse(to_)
            # range1 = (range1start, range1end)

            c = quasardb.Cluster('qdb://127.0.0.1:2836')
            ts = c.ts("dummy")

            col1 = ts.column(quasardb.TimeSeries.DoubleColumnInfo("col1"))

            range1start = dt.datetime.now(quasardb.tz) - timedelta(days=3)
            range1end = dt.datetime.now(quasardb.tz) + timedelta(days=2)

            range1 = (range1start, range1end)
            results = col1.get_ranges([range1])
            res = json.dumps(results, default=json_serializer)
            data = json.loads(res)
            grafana_data = []

            for i in xrange(0, len(data)):
                grafana_data.append([int(data[i][1]), int(data[i][0])])

            return [{'target': 'temperatures', 'datapoints': grafana_data}]
        else:
            return { 'error' : 'No range given for timeserie or missing target(s)' }

    def update(self):
        return {'message' : '[UPDATE] is not supported'}

    def delete(self):
        return {'message' : '[DELETE] is not supported'}
