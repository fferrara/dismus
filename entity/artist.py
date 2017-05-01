__author__ = 'Flavio Ferrara'

class Artist():
    def __init__(self, name, thumb_url):
        self.name = name
        self.thumb_url = thumb_url
        self.type = 'ARTIST'

    def __repr__(self):
        return {
            'type': self.type,
            'name': self.name,
            'thumb_url': self.thumb_url
        }

    def toDTO(self):
        return self.__repr__()