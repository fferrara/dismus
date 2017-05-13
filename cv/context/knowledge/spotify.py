import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from entity.artist import Artist
from ..knowledge.source import KnowledgeSource
from shared.exceptions import ArtistNotFoundException

__author__ = 'Flavio Ferrara'


class SpotifySource(KnowledgeSource):
    def get_related_artists(self, artist_id):
        """


        :rtype : list of Artist
        :param artist_name:
        :return: List
        :raise ArtistNotFoundException:
        """
        results = self.spotify.artist_related_artists(artist_id)
        artists = results['artists']

        return [self._create_artist(a) for a in artists]

    def __init__(self):
        self.credential_manager = SpotifyClientCredentials()
        self.spotify = spotipy.Spotify(client_credentials_manager=self.credential_manager)

    def getPlaylistByArtist(self, artist_names):
        if isinstance(artist_names, str):
            artist_names = [artist_names]

        artists = [self.get_artist(name) for name in artist_names]
        seeds = [artist['id'] for artist in artists if artist is not None]

        results = self.spotify.recommendations(seed_artists = seeds)
        return results


    def getByGenre(self, genre_name):
        pass

    def getByTrack(self, tracks):
        pass

    def get_artist(self, artist_name):
        """

        :param artist_name:
        :return: an artist object
        :rtype: Artist
        """
        results = self.spotify.search(q='artist:' + artist_name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return self._create_artist(items[0])
        else:
            return None

    def _create_artist(self, artist_dict):
        try:
            thumb_url = next(img['url'] for img in artist_dict['images'] if img['height'] < 400)
        except StopIteration:
            thumb_url = artist_dict['images'][-1]['url']
        return Artist(artist_dict['name'], thumb_url, spotify_id=artist_dict['id'])