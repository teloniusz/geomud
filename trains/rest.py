from flask import Flask, jsonify
from flask_restful import Resource, Api
from trains import Trains


app = Flask(__name__)
api = Api(app)
trains = Trains()

# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq


class TrainAPI(Resource):
    def get(self):
        return jsonify(trains.get_trains())

api.add_resource(TrainAPI, '/trains')
