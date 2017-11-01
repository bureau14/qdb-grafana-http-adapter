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

            cluster = app.config.get('QDB_CLUSTER_URI', None)
            if cluster != None:
                c = quasardb.Cluster(cluster)
                timeseries = app.config.get('TIMESERIES', [])
                grafana_data = []

                from_ = range_.get('from', None)
                to_ = range_.get('to', None)
                range1start = dateutil.parser.parse(from_)
                range1end = dateutil.parser.parse(to_)

                for t in targets:
                    for ts_ in timeseries:
                        if ts_ == t.get('target'):
                            print ts_
                            ts = c.ts(ts_)
                            col1 = ts.column(quasardb.TimeSeries.DoubleColumnInfo("col_grafana"))
                            range1 = (range1start, range1end)
                            results = col1.get_ranges([range1])
                            res = json.dumps(results, default=json_serializer)
                            data = json.loads(res)
                            datapoints = []
                            for i in xrange(0, len(data)):
                                datapoints.append([int(data[i][1]), int(data[i][0])])
                            grafana_data.append({'target': ts_, 'datapoints': datapoints})
                return grafana_data
        else:
            return { 'error' : 'No range given for timeserie or missing target(s)' }

    def update(self):
        return {'message' : '[UPDATE] is not supported'}

    def delete(self):
        return {'message' : '[DELETE] is not supported'}
