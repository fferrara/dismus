import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ..knowledge.source import KnowledgeSource
from shared.exceptions import ArtistNotFoundException

__author__ = 'Flavio Ferrara'


class SpotifySource(KnowledgeSource):
    def getRelatedArtists(self, artist_name):
        artist = self._get_artist(artist_name)
        if artist is None:
            raise ArtistNotFoundException

        results = self.spotify.artist_related_artists(artist['id'])
        artists = results['artists']

        return [a['name'] for a in artists]

    def __init__(self):
        self.credential_manager = SpotifyClientCredentials()
        self.spotify = spotipy.Spotify(client_credentials_manager=self.credential_manager)

    def getPlaylistByArtist(self, artist_names):
        if isinstance(artist_names, str):
            artist_names = [artist_names]

        artists = [self._get_artist(name) for name in artist_names]
        seeds = [artist['id'] for artist in artists if artist is not None]

        results = self.spotify.recommendations(seed_artists = seeds)
        return results


    def getByGenre(self, genre_name):
        pass

    def getByTrack(self, tracks):
        pass

    def _get_artist(self, artist_name):
        results = self.spotify.search(q='artist:' + artist_name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return items[0]
        else:
            return None