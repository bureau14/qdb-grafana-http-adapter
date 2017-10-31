from flask_restful import Resource, reqparse
from flask import current_app as app, request
import json
import os

class SearchCtrl(Resource):

    def get(self):
        return {'message' : '[GET] is not supported'}

    def post(self):
        return app.config.get('TIMESERIES')

    def update(self):
        return {'message' : '[UPDATE] is not supported'}

    def delete(self):
        return {'message' : '[DELETE] is not supported'}
