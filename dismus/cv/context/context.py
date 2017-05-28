from dismus.cv.context.knowledge.spotify import SpotifySource
from dismus.entity.artist import ArtistsHint
from dismus.entity.track import TracksHint

__author__ = 'Flavio Ferrara'


class KnowledgeSourceFactory():
    @staticmethod
    def create():
        return SpotifySource()


class ContextManager():
    def __init__(self):
        """
        Context Manager stores the context for a given conversation.
        This includes the set of artists/tracks the user like, dislikes, already mentioned.

        Data about music comes from a Knowledge Source.

        """
        self.tracks = set()
        self.artists = set()
        self.artist_likes = set()
        self.artist_dislikes = set()
        self.source = KnowledgeSourceFactory.create()
        self.flags = {}

    @property
    def artist_know(self):
        return self.artists | self.artist_dislikes | self.artist_likes

    def set_flag(self, setter):
        """

        :param str setter:
        """
        self.flags[setter] = True

    def is_flag(self, flag):
        return self.flags.get(flag, False)

    def get_related_artists(self, artist_id):
        """
        Retrieve all Artists related to the Artist called artist_name
        :param artist_name:
        :return:
        """
        hint = ArtistsHint()
        return [hint] + self.__get_related_artists(artist_id)

    def like_artist(self, artist_id):
        """
        User likes the Artists identified by artist_id

        :param artist_id:
        :return:
        """
        self.artist_likes.add(artist_id)
        self.artists.add(artist_id)

        return self.__get_related_artists(artist_id)

    def __get_related_artists(self, artist_id):
        related = self.source.get_related_artists(artist_id=artist_id)
        novel = [artist for artist in related
                   if artist.id not in self.artist_know]
        self.artists.update([artist.id for artist in novel])
        return sorted(novel, key=lambda a: a.popularity, reverse=True)

    def get_tracks_for_artist(self, artist_ids):
        """
        Retrieve a collection of Tracks based on Artists identified by artist_ids
        :param artist_ids:
        :return:
        """
        self.artists.update(artist_ids)

        tracks = self.source.get_playlist_by_artists(artist_ids)
        return self.__novel_tracks(tracks)

    def get_by_track(self, track_id):
        """
        Retrieve a collection of Tracks related to the Track identified by track_id
        :param track_ids:
        """
        hint = TracksHint()
        return [hint] + self.get_tracks_for_tracks([track_id])

    def get_tracks_for_tracks(self, track_ids):
        """
        Retrieve a collection of Tracks based on Tracks identified by track_ids
        :param artist_ids:
        :return:
        """
        self.tracks.update(track_ids)

        tracks = self.source.get_playlist_by_tracks(track_ids)
        return self.__novel_tracks(tracks)

    def __novel_tracks(self, tracks):
        novels = [track for track in tracks if track.id not in self.tracks]
        self.tracks.update([track.id for track in novels])
        return novels