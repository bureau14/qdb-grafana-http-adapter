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
            separator = app.config.get('SEPARATOR_TS_LABEL', None)
            tag_grafana = app.config.get('TAG_TS_GRAFANA', None)

            if cluster != None and separator != None and tag_grafana != None:
                c = quasardb.Cluster(cluster)
                tag = c.tag(tag_grafana)
                timeseries = list(tag.get_entries())
                grafana_data = []

                from_ = range_.get('from', None)
                to_ = range_.get('to', None)
                range1start = dateutil.parser.parse(from_)
                range1end = dateutil.parser.parse(to_)

                timeseries = []
                # Grabbing all timeseries tagged with 'grafana' tag
                tag = c.tag(tag_grafana)
                entries = list(tag.get_entries())
                for entry in entries:
                    ts = c.ts(entry)
                    cols = ts.columns_info()
                    cols_name = []
                    for col in cols:
                        name = entry + separator + col.name
                        timeseries.append(name)

                # looping over targets returning datapoints for selected entries
                for t in targets:
                    for ts in timeseries:
                        if ts == t.get('target'):
                            ts_ = c.ts(ts.split(separator)[0])
                            col_ = ts.split(separator)[1]
                            col_selected = ts_.column(quasardb.TimeSeries.DoubleColumnInfo(col_))
                            range1 = (range1start, range1end)
                            results = col_selected.get_ranges([range1])
                            res = json.dumps(results, default=json_serializer)
                            data = json.loads(res)
                            datapoints = []
                            for i in xrange(0, len(data)):
                                datapoints.append([int(data[i][1]), int(data[i][0])])
                            grafana_data.append({'target': ts, 'datapoints': datapoints})
            return grafana_data
        else:
            return { 'error' : 'No range given for timeserie or missing target(s)' }

    def update(self):
        return {'message' : '[UPDATE] is not supported'}

    def delete(self):
        return {'message' : '[DELETE] is not supported'}
