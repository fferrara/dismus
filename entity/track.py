from entity.album import Album
from entity.artist import Artist

__author__ = 'Flavio Ferrara'


class Track():
    def __init__(self, name, preview_url, artist, album, spotify_id):
        self.artist = artist
        self.album = album
        self.spotify_id = spotify_id
        self.name = name
        self.preview_url = preview_url
        self.popularity = None
        self.type = 'TRACK'

    def __repr__(self):
        return {
            'type': self.type,
            'artist': self.artist.__repr__(),
            'album': self.album.__repr__(),
            'name': self.name,
            'url': self.url,
            'id': self.spotify_id
        }

    @property
    def id(self):
        if self.spotify_id is not None:
            return self.spotify_id

    @property
    def url(self):
        return self.preview_url

    def toDTO(self):
        return self.__repr__()

    @classmethod
    def build(cls, data_dict):
        return Track(
            data_dict['name'],
            data_dict['preview_url'],
            Artist.build(data_dict['artists'][0]),
            Album.build(data_dict['album']),
            data_dict['id']
        )