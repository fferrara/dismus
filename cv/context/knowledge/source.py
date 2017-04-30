__author__ = 'Flavio Ferrara'

from abc import ABC


class KnowledgeSource(ABC):
    def getByGenre(self, genre_name):
        raise NotImplementedError("Class %s doesn't implement getByGenre()" % self.__class__.__name__)

    def getPlaylistByArtist(self, artist_names):
        raise NotImplementedError("Class %s doesn't implement getByArtist()" % self.__class__.__name__)

    def getRelatedArtists(self, artist_name):
        raise NotImplementedError("Class %s doesn't implement getByArtist()" % self.__class__.__name__)

    def getByTrack(self, tracks):
        raise NotImplementedError("Class %s doesn't implement getByTrack()" % self.__class__.__name__)