from abc import ABC
from cv.context.knowledge.spotify import SpotifySource
from entity.artist import ArtistsHint

__author__ = 'Flavio Ferrara'


class KnowledgeSourceFactory():
    @staticmethod
    def create():
        return SpotifySource()


class ContextManager():
    def __init__(self):
        self.artists = []
        self.artist_likes = []
        self.artist_dislikes = []
        self.source = KnowledgeSourceFactory.create()
        self.flags = {}

    @property
    def artist_know(self):
        return self.artist_dislikes+self.artist_likes

    def set_flag(self, setter):
        """

        :param str setter:
        """
        self.flags[setter] = True

    def is_flag(self, flag):
        return self.flags.get(flag, False)

    def get_related_artists(self, artist_name):
        artist = self.source.get_artist(artist_name)
        related = self.source.get_related_artists(artist.id)
        return ArtistsHint(self.__store_artists(related))

    def like_artist(self, artist_id):
        self.artist_likes.append(artist_id)
        self.artists.append(artist_id)
        related = self.source.get_related_artists(artist_id=artist_id)

        return ArtistsHint(self.__store_artists(related))

    def __store_artists(self, related_artists):
        uniques = [artist for artist in related_artists
                         if artist.id not in self.artist_know + self.artists]

        self.artists.extend([artist.id for artist in uniques])
        return uniques