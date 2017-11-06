from flask_restful import Resource, reqparse
from flask import current_app as app, request
import json
import os
import quasardb

class SearchCtrl(Resource):

    def get(self):
        return {'message' : '[GET] is not supported'}

    def post(self):
        cluster_uri = app.config.get('QDB_CLUSTER_URI', None)
        separator = app.config.get('SEPARATOR_TS_LABEL', None)

        if cluster_uri != None and separator != None:
            cluster = quasardb.Cluster(cluster_uri)
            tag = cluster.tag('grafana')
            entries = list(tag.get_entries())
            results = []
            for entry in entries:
                ts = cluster.ts(entry)
                cols = ts.columns_info()
                cols_name = []
                for col in cols:
                    name = entry + separator + col.name
                    result = {"text": name, "value": name}
                    results.append(result)
            return results

    def update(self):
        return {'message' : '[UPDATE] is not supported'}

    def delete(self):
        return {'message' : '[DELETE] is not supported'}
