from flask import Flask, request
from flask_restful import Resource, Api

from wikiget import Wiki


class WikiRest(Resource):
    def get(self, title, lon=None, lat=None):
        if lon and lat:
            return Wiki().get_coords(lat, lon, full=True)
        return Wiki().get_page(title)


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(WikiRest,
                     '/page/<string:title>', '/page/<float:lon>,<float:lat>,<string:title>')
    return app


app = create_app()
