from dismus.entity.album import Album
from dismus.entity.artist import Artist
from dismus.entity.entity import MusicEntity

__author__ = 'Flavio Ferrara'


class Track(MusicEntity):
    def __init__(self, name, preview_url, artist, album, spotify_id):
        self.artist = artist
        self.album = album
        self.spotify_id = spotify_id
        self.name = name
        self.preview_url = preview_url
        self.popularity = None
        self.type = 'TRACK'

    def __repr__(self):
        return str(self.serialize())

    @property
    def id(self):
        if self.spotify_id is not None:
            return self.spotify_id

    @property
    def url(self):
        return self.preview_url

    def serialize(self):
        return {
            'type': self.type,
            'artist': self.artist.serialize(),
            'album': self.album.serialize(),
            'name': self.name,
            'url': self.url,
            'id': self.spotify_id
        }

    @classmethod
    def build(cls, data_dict):
        return Track(
            data_dict['name'],
            data_dict['preview_url'],
            Artist.build(data_dict['artists'][0]),
            Album.build(data_dict['album']),
            data_dict['id']
        )