from entity.artist import Artist

__author__ = 'Flavio Ferrara'


class Album():
    def __init__(self, name, thumb_url, artist, spotify_id):
        self.spotify_id = spotify_id
        self.name = name
        self.thumb_url = thumb_url
        self.artist = artist
        self.popularity = None
        self.type = 'ARTIST'

    def __repr__(self):
        return {
            'type': self.type,
            'name': self.name,
            'artist': self.artist.__repr__(),
            'thumb_url': self.thumb_url or '',
            'id': self.spotify_id
        }

    @property
    def id(self):
        if self.spotify_id is not None:
            return self.spotify_id

    def toDTO(self):
        return self.__repr__()

    @classmethod
    def build(cls, album_dict):
        try:
            thumb_url = next(img['url'] for img in album_dict['images'] if img['height'] < 400)
        except StopIteration:
            thumb_url = album_dict['images'][-1]['url']
        except KeyError:
            thumb_url = None

        a = Album(
            album_dict['name'],
            thumb_url,
            Artist.build(album_dict['artists'][0]),
            spotify_id=album_dict['id'])
        a.popularity = album_dict.get('popularity', None)

        return a


class ArtistsHint():

    def __repr__(self):
        return {
            'type': 'HINT'
        }

    def toDTO(self):
        return self.__repr__()