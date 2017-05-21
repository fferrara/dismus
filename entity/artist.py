__author__ = 'Flavio Ferrara'


class Artist():
    def __init__(self, name, thumb_url, spotify_id):
        self.spotify_id = spotify_id
        self.name = name
        self.thumb_url = thumb_url
        self.popularity = None
        self.type = 'ARTIST'

    def __repr__(self):
        return str(self.toDTO())

    @property
    def id(self):
        if self.spotify_id is not None:
            return self.spotify_id

    def toDTO(self):
        return {
            'type': self.type,
            'name': self.name,
            'thumb_url': self.thumb_url or '',
            'id': self.spotify_id
        }

    @classmethod
    def build(cls, artist_dict):
        try:
            thumb_url = next(img['url'] for img in artist_dict['images'] if img['height'] < 400)
        except StopIteration:
            thumb_url = artist_dict['images'][-1]['url']
        except KeyError:
            thumb_url = None

        a = Artist(artist_dict['name'], thumb_url, spotify_id=artist_dict['id'])
        a.popularity = artist_dict.get('popularity', None)

        return a


class ArtistsHint():

    def __repr__(self):
        return str(self.toDTO())

    def toDTO(self):
        return {
            'type': 'HINT',
            'hint': 'ARTISTS',
        }