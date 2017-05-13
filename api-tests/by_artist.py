from unittest.case import TestCase
import json
from websocket import create_connection

__author__ = 'Flavio Ferrara'

class ByArtistTest(TestCase):

    def setUp(self):
        self.ws = create_connection("ws://localhost:9000")

    def testRelatedArtists(self):
        data = {
            'type': 'CHOICE',
            'text': 'Artist'
        }
        self.ws.send(json.dumps(data))
        result = self.ws.recv()
        print (result)