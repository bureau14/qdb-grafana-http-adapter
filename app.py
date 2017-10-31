from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from api import query, search, annotations

app = Flask(__name__)
app.config.from_object('settings') # settings.py

CORS(app, resources={r"/": {"origins": "*"}})
CORS(app, resources={r"/query": {"origins": "*"}})
CORS(app, resources={r"/search": {"origins": "*"}})
CORS(app, resources={r"/annotations": {"origins": "*"}})

api = Api(app)
api.add_resource(query.QueryCtrl, '/query')
api.add_resource(search.SearchCtrl, '/search')
api.add_resource(annotations.AnnotationsCtrl, '/annotations')

@app.route('/')
def default_route():
    return 'Grafana API is running'

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', app.config['PORT_API'], app)
    httpd.serve_forever()
