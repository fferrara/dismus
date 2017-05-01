from abc import ABC
from cv.context.knowledge.spotify import SpotifySource

__author__ = 'Flavio Ferrara'


class KnowledgeSourceFactory():
    @staticmethod
    def create():
        return SpotifySource()


class ContextManager():
    def __init__(self):
        self.source = KnowledgeSourceFactory.create()
        self.flags = {}

    def set_flag(self, setter):
        """

        :param str setter:
        """
        self.flags[setter] = True

    def is_flag(self, flag):
        return self.flags.get(flag, False)

    def getRelatedArtists(self, artist_name):
        return self.source.getRelatedArtists(artist_name)

    def execute_trigger(self, trigger, param):
        trigger_handler = getattr(self, trigger)
        return trigger_handler(param)


