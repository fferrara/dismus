__author__ = 'Flavio Ferrara'


class Artist():
    def __init__(self, name, thumb_url, spotify_id):
        self.spotify_id = spotify_id
        self.name = name
        self.thumb_url = thumb_url
        self.type = 'ARTIST'

    def __repr__(self):
        return {
            'type': self.type,
            'name': self.name,
            'thumb_url': self.thumb_url,
            'id': self.spotify_id
        }

    @property
    def id(self):
        if self.spotify_id is not None:
            return self.spotify_id

    def toDTO(self):
        return self.__repr__()


class ArtistsHint():
    def __init__(self, artists):
        self.artists = artists

    def __repr__(self):
        return {
            'type': 'ARTISTS',
            'artists': [artist.toDTO() for artist in self.artists]
        }

    def toDTO(self):
        return self.__repr__()