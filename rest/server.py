from flask.ext.cors import CORS
from flask import Flask

__author__ = 'Flavio Ferrara'

app = Flask(__name__)
CORS(app)

class DisMusRest:
    def __init__(self, context):
        self.context = context
        self.app = app

        self.app.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.app.add_url_rule('/artists/<artist_id>/likes',
                              view_func=self.like_artist, methods=['PUT', 'POST'])

    def run(self):
        self.app.run()

    def index(self):
        return 'Hello World!'

    def like_artist(self, artist_id):
        print('like {}'.format(artist_id))
        return 'a'
