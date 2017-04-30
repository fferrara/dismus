from cv.context.knowledge.spotify import SpotifySource

__author__ = 'Flavio Ferrara'


class KnowledgeSourceFactory():
    @staticmethod
    def create():
        return SpotifySource()


class ContextManager():
    def __init__(self):
        self.source = KnowledgeSourceFactory.create()

    def getRelatedArtists(self, artist_name):
        return self.source.getRelatedArtists(artist_name)


