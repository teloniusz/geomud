import os
import time
from flask import Flask
from flask_restful import Resource, Api

from model import LocBackend


class Location(Resource):
    def get(self, name=None, loc_id=None):
        try:
            return next(LocBackend.instance().get_place(name=name, lau_code=loc_id, county=True))
        except StopIteration:
            return None


class Neighbors(Resource):
    def get(self, loc_id=None, name=None):
        return LocBackend.instance().get_neighbors(name=name, lau_code=loc_id)


class County(Resource):
    def get(self, longitude, latitude):
        return LocBackend.instance().get_county([longitude, latitude])


def create_app():
    app = Flask(__name__)
    api = Api(app)
    pg_user, pg_pass, pg_db, pg_host = (
        os.environ[f'POSTGRES_{key}']
        for key in ('USER', 'PASS', 'DB', 'HOST'))
    LocBackend.connect_string = f'postgresql://{pg_user}:{pg_pass}@{pg_host}/{pg_db}'
    api.add_resource(Location, '/location/<string:name>', '/location/<int:loc_id>')
    api.add_resource(Neighbors, '/neighbors/<string:name>', '/neighbors/<int:loc_id>')
    api.add_resource(County, '/county/<float:longitude>,<float:latitude>')
    return app


app = create_app()
