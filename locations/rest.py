from flask import Flask, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)
db_connect = create_engine('postgresql://astrouter:astrtt@172.17.0.1/astrouter')
db = db_connect.connect()

# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq


class Locations(Resource):
    def get(self):
        query = db.execute('SELECT * FROM clients')
        return {'clients': [dict(zip(tuple(query.keys()), str(i))) for i in query.cursor]}

api.add_resource(Locations, '/location/')
