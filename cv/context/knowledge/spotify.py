import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from entity.artist import Artist
from entity.track import Track
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

        return [Artist.build(a) for a in artists]

    def __init__(self):
        self.credential_manager = SpotifyClientCredentials()
        self.spotify = spotipy.Spotify(client_credentials_manager=self.credential_manager)

    def get_playlist_by_artists(self, artist_ids):
        if isinstance(artist_ids, str):
            artist_ids = [artist_ids]

        if len(artist_ids) > 5:
            artist_ids = artist_ids[0:5]

        results = [Track.build(t) for t in self.spotify.recommendations(seed_artists = artist_ids)['tracks']]
        print(results[0].toDTO())
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
            return Artist.build(items[0])
        else:
            return None

    def get_popular_tracks_for_artist(self, artist_id):
        pass

