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
        if cluster_uri != None:
            cluster = quasardb.Cluster(cluster_uri)
            tag = cluster.tag('grafana')
            return list(tag.get_entries())

    def update(self):
        return {'message' : '[UPDATE] is not supported'}

    def delete(self):
        return {'message' : '[DELETE] is not supported'}
