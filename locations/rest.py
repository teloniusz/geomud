import os
import time
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine


class Locations(Resource):
    def get(self):
        query = db.execute('SELECT * FROM clients')
        return {'clients': [dict(zip(tuple(query.keys()), str(i))) for i in query.cursor]}


def create_app():
    app = Flask(__name__)
    api = Api(app)
    pg_user, pg_pass, pg_host, pg_db = (
        os.environ[key]
        for key in ('POSTGRES_USER', 'POSTGRES_PASS', 'POSTGRES_DB', 'POSTGRES_HOST'))
    db_connect = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}/{pg_db}')
    db = db_connect.connect()
# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
    api.add_resource(Locations, '/location/')

    return app, db


app, db = create_app()
