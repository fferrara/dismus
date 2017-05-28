import json

from flask.ext.cors import CORS
from flask import Flask, request


__author__ = 'Flavio Ferrara'

app = Flask(__name__)
CORS(app)

class DisMusRest:
    def __init__(self, context):
        """

        :param ContextManager context:
        """
        self.context = context  # type: ContextManager
        self.app = app

        self.app.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.app.add_url_rule('/play',
                              view_func=self.play_artists, methods=['POST'])

    def run(self):
        self.app.run()

    def index(self):
        return 'Hello World!'

    def play_artists(self):
        body = request.get_json()
        print('play {}'.format(body))
        tracks = self.context.get_tracks_for_artist(body['artists'])

        a = json.dumps([track.serialize() for track in tracks])

        return a
